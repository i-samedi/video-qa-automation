from moviepy.editor import VideoFileClip
import streamlit as st

def extract_audio(video_file):
    try:
        with st.spinner("Extracting audio..."):
            video = VideoFileClip(video_file)
            audio = video.audio
            audio_file = "extracted_audio.ogg"
            audio.write_audiofile(audio_file, codec='libvorbis')
            video.close()
    except Exception as e:
        st.error(f"Error extracting audio: {str(e)}")