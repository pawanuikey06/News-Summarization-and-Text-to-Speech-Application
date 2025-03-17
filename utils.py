import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage


def scrape_news(company_name):
    """
    Scrape news articles related to the given company name from Google News RSS.
    """
    # Google News RSS URL (Non-JS)
    url = f"https://news.google.com/rss/search?q={company_name}"

    # Send a GET request
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve news. Status code: {response.status_code}")
        return []
    
    # Parse XML response using BeautifulSoup
    soup = BeautifulSoup(response.content, "xml")

    # Extract all news items
    items = soup.find_all("item")[:10]  # Limit to 10 articles

    news_data = []
    for item in items:
        title = item.title.text
        link = item.link.text
        source = item.source.text if item.source else "Unknown"
        timestamp = item.pubDate.text

        news_data.append({
            "Title": title,
            "Link": link,
            "Source": source,
            "Timestamp": timestamp
        })

    return news_data

# def display_news(news_data):
#     """Display the scraped news data."""
#     if not news_data:
#         print("No news articles found.")
#         return
    
#     df = pd.DataFrame(news_data)
#     print(df)


def summarize_with_mistral(article):

    """
    mistral AI for summarization
    """
    load_dotenv()
    api_key =os.getenv("MISTRAL_API_KEY")

    model =ChatMistralAI(api_key=api_key,model="mistral-large-latest")

    system_message =SystemMessage(content="You are an AI Assistant that Summarizes articles")

    chat_history=[system_message,HumanMessage(content=f"A concise summary for the folloing article:\n\n {article}")]

    result =model.invoke(chat_history)
    summary=result.content


    





if __name__ == "__main__":
    company_name = "Tesla"  # Replace with any company name
    process_news(company_name)
    
