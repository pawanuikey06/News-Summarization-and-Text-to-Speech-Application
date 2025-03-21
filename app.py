import streamlit as st
import requests
import base64
import tempfile

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
            speech_base64 = result["Analysis"]["Final Sentiment Analysis"].get("speech", "")
            if speech_base64:
                audio_bytes = base64.b64decode(speech_base64.split(",")[1])

                # Save the audio to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_audio_path = tmp_file.name

                # Play the audio in Streamlit
                st.audio(tmp_audio_path, format="audio/mp3")
            
        else:
            st.write(f"Error {response.status_code}: {response.text}")
    else:
        st.write("Please enter a company name.")
