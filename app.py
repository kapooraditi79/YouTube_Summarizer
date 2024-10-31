import streamlit as st
from dotenv import load_dotenv

load_dotenv()       #loads all the environment variable

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


from youtube_transcript_api import YouTubeTranscriptApi
#This api is responsible for getting the transcript of the entire youtube video
#but the youtube video must be public


prompt="""You are a Youtube Video Summarizer. You will be taking the transcript text
 and summarizing the entire video and providing the important summary in points
 within 350 words. The following is the transcript text: """

#getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        #split() puts the url into 2 parts: one before the equal to and having "=", one after the "="
        #the second part is what we need
        #that is the youtube video id
        transcript_extracted=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_extracted:
            transcript+= " " + i["text"]
        return transcript
    
    except Exception as e:
        raise e


#getting the summary based on prompt from google gemini pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt + transcript_text)
    return response.text




st.title("Youtube transcript Summarizer")
youtube_link=st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text= extract_transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text, prompt)
        st.markdown("Detailed Summary:")
        st.write(summary)