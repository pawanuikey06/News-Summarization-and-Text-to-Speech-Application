import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from yake import KeywordExtractor
from collections import Counter
from transformers import pipeline


nltk.download('vader_lexicon')

def scrape_news(company_name):
    try:
        url = f"https://news.google.com/rss/search?q={company_name}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:10]
        return [{
            "Title": item.title.text,
            "Link": item.link.text,
            "Source": item.source.text if item.source else "Unknown",
            "Timestamp": item.pubDate.text
        } for item in items]
    except Exception as e:
        print(f"Error in scraping news: {e}")
        return []
# def display_news(news_data):
#     """Display the scraped news data."""
#     if not news_data:
#         print("No news articles found.")
#         return
    
#     df = pd.DataFrame(news_data)
#     print(df)

def summarize_with_mistral(article):
    try:
        load_dotenv()
        api_key = os.getenv("MISTRAL_API_KEY")
        model = ChatMistralAI(api_key=api_key, model="mistral-large-latest")
        chat_history = [
            SystemMessage(content="You are an AI Assistant that Summarizes articles"),
            HumanMessage(content=f"A concise summary for the following article and do not include summary word and only three Lines no extra headings:\n\n{article}")
        ]
        return model.invoke(chat_history).content
    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Summary Not Available"


def analyze_sentiment_vader(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)

    if sentiment['compound'] > 0.05:
        return "Positive"
    elif sentiment['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"
    
def extract_topics(text, num_topics=3):
    extractor = KeywordExtractor(n=2, top=num_topics)  # Extract 1-2 word phrases
    keywords = extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def comparative_analysis(news_data):
    """
    Perform comparative sentiment analysis and topic comparison.

    Parameters:
    news_data (list): List of dictionaries containing 'Title', 'Summary', 'Sentiment', and 'Topics'.

    Returns:
    dict: A structured comparative analysis.
    """
    sentiment_counts = Counter([article["Sentiment"] for article in news_data])
    total_articles = len(news_data)

    # Sentiment Distribution
    sentiment_distribution = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
    }

    # Compare articles based on their themes and impacts
    coverage_differences = []
    for i in range(len(news_data) - 1):
        comparison = {
            "Comparison": f"Article {i+1} discusses '{news_data[i]['Topics']}', while Article {i+2} focuses on '{news_data[i+1]['Topics']}'.",
            "Impact": f"One article highlights '{news_data[i]['Sentiment']}' aspects, while the other brings '{news_data[i+1]['Sentiment']}' points, influencing perception accordingly."
        }
        coverage_differences.append(comparison)

    # Extract common and unique topics
    all_topics = [set(article["Topics"]) for article in news_data]
    common_topics = set.intersection(*all_topics) if all_topics else set()
    unique_topics_per_article = [
        {
            f"Unique Topics in Article {i+1}": list(all_topics[i] - common_topics)
        }
        for i in range(len(all_topics))
    ]

    #  Final Sentiment Analysis Summary
    if sentiment_distribution["Positive"] > sentiment_distribution["Negative"]:
        final_analysis = "Tesla’s latest news coverage is mostly positive."
    elif sentiment_distribution["Negative"] > sentiment_distribution["Positive"]:
        final_analysis = "Tesla is currently facing negative media attention."
    else:
        final_analysis = "Tesla’s news coverage is balanced with neutral perception."


    comparative_analysis_result = {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_distribution,
            "Coverage Differences": coverage_differences,
            "Topic Overlap": {
                "Common Topics": list(common_topics),
                "Unique Topics per Article": unique_topics_per_article
            }
        },
        "Final Sentiment Analysis": final_analysis
    }

    return comparative_analysis_result
    




def process_news(company_name):
    try:
        news_data = scrape_news(company_name)
        if not news_data:
            print("No news articles found.")
            return
        report = {
            "Company": company_name,
            "Articles": []
        }
        for article in news_data:
            
            summary = summarize_with_mistral(article["Title"]) if article['Title'] else "Summary Not Available"
            # print(summary)
            sentiment =analyze_sentiment_vader(summary)
            topics =extract_topics(summary)
            # print(topics)
            report["Articles"].append({
                "Title": article["Title"],
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics
            })
        analysis=comparative_analysis(report["Articles"])
        report["Analysis"] = analysis 
        return report
        # print(report)
    except Exception as e:
        print(f"Error processing news: {e}")


    

