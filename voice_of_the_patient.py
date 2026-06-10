# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    audio_filepath="patient_voice_test_for_patient.mp3"
    #record_audio(file_path=audio_filepath)

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq_helper import execute_with_fallback

stt_model="whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY=None):
    # Safeguard: Check if the audio file size is too small or empty (e.g. under 2KB)
    if os.path.exists(audio_filepath) and os.path.getsize(audio_filepath) < 2000:
        logging.warning("Audio file is too small or empty. Using default query.")
        return "Please analyze this image and suggest any medical remedies."

    def _transcribe(client):
        with open(audio_filepath, "rb") as audio_file:
            transcription=client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text

    try:
        return execute_with_fallback(_transcribe)
    except Exception as e:
        logging.error(f"All keys failed during Groq transcription: {e}")
        return "Please analyze this image and suggest any medical remedies."
