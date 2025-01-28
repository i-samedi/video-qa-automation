import streamlit as st
from openai import OpenAI
from datetime import timedelta
from service.glossary import GLOSSARY, apply_glossary
import os

# Add this new function to extract transcript using Whisper
def extract_transcript(audio_file_path):
    try:
        client = OpenAI(
            base_url="https://api.openai.com/v1"
        )

        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

            # Crear un prompt que incluya el glosario
            glossary_terms = "\n".join([f"- {term}: {obj.term} (variations: {', '.join(obj.variations)})"
                                      for term, obj in GLOSSARY.items()])

            prompt = f"""Transcribe this audio efficiently with these exact requirements:
                - Format: {{Speaker}}{{HH:MM:SS}} Text
                - Detect speakers automatically (Person1, Person2, etc.)
                - Include precise timestamps
                - Process in chunks for speed
                - Focus on accuracy of speaker detection and timing
                - Pay special attention to letters and numbers
                - Distinguish between similar sounding letters (e.g., B/V, M/N)
                - Clearly separate words and maintain proper spacing

                Use this glossary for specific terms:
                {glossary_terms}

                When you encounter any of these terms or their variations, use the correct form from the glossary."""

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.ogg", audio_data, "audio/ogg"),
                response_format="verbose_json",
                prompt=prompt
            )

        # Procesar el transcript con el glosario
        formatted_transcript = []

        if hasattr(transcript, 'segments'):
            segments = transcript.segments
        elif isinstance(transcript, dict) and 'segments' in transcript:
            segments = transcript['segments']
        else:
            st.warning("Unexpected response format. Using raw transcript.")
            segments = [{'start': 0, 'text': transcript.text if hasattr(transcript, 'text') else str(transcript)}]

        current_speaker = "Person1"

        for segment in segments:
            start_time = segment.get('start', 0) if isinstance(segment, dict) else getattr(segment, 'start', 0)
            text = segment.get('text', '') if isinstance(segment, dict) else getattr(segment, 'text', '')

            if isinstance(segment, dict) and 'speaker' in segment:
                current_speaker = segment['speaker']

            start_timedelta = timedelta(seconds=float(start_time))
            formatted_time = f"{{00:{start_timedelta.seconds//3600:02d}:{(start_timedelta.seconds//60)%60:02d}:{start_timedelta.seconds%60:02d}}}"

            cleaned_text = text.strip()
            if cleaned_text:
                # Aplicar el glosario al texto
                cleaned_text = apply_glossary(cleaned_text)
                formatted_line = f"{{{current_speaker}}}{formatted_time} {cleaned_text}"
                formatted_transcript.append(formatted_line)

        # Guardar la transcripción formateada
        with open("extracted_transcript.txt", "w", encoding="utf-8") as transcript_file:
            transcript_file.write("\n".join(formatted_transcript))

        st.success("Transcripción guardada como 'extracted_transcript.txt'")

    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        st.error("Detailed error information")
        st.error(f"API Key status: {'Present' if client.api_key else 'Missing'}")
        if hasattr(e, 'response'):
            st.error(f"Response status: {e.response.status_code}")
            st.error(f"Response content: {e.response.text}")