import streamlit as st
import requests

# FastAPI URL
API_URL = "http://127.0.0.1:8000/analyze_news"

# Streamlit UI to input company name
st.title(" News Summarization and Text-to-Speech Application")

company_name = st.text_input("Enter company name")

if st.button("Analyze"):
    if company_name:
        # Make a POST request to FastAPI
        response = requests.post(API_URL, json={"company_name": company_name})

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()

            # Display the result on the Streamlit UI
            st.write("Full API Response:", result)
            
            
        else:
            st.write(f"Error {response.status_code}: {response.text}")
    else:
        st.write("Please enter a company name.")
