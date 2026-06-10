import os
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import logic from existing scripts
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

load_dotenv()

app = FastAPI(title="AI Doctor 2.0 Professional API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
from groq_helper import get_groq_keys, get_gemini_keys, get_openrouter_keys, get_together_keys, get_hf_keys, get_mistral_keys
groq_keys = get_groq_keys()
gemini_keys = get_gemini_keys()
openrouter_keys = get_openrouter_keys()
together_keys = get_together_keys()
hf_keys = get_hf_keys()
mistral_keys = get_mistral_keys()

if not any([groq_keys, gemini_keys, openrouter_keys, together_keys, hf_keys, mistral_keys]):
    raise ValueError("No API keys found. You must set at least one provider key (GROQ_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY, TOGETHER_API_KEY, HF_TOKEN, or MISTRAL_API_KEY) in .env.")

GROQ_API_KEY = groq_keys[0] if groq_keys else None

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

@app.post("/api/process")
async def process_consultation(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
    model: str = Form("groq-llama4")
):
    """
    Process both image and audio to get doctor's response and TTS.
    """
    try:
        # Save uploaded files temporarily
        image_path = os.path.join(TEMP_DIR, image.filename)
        audio_path = os.path.join(TEMP_DIR, audio.filename)
        
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # 1. Transcribe audio
        transcription = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY,
            audio_filepath=audio_path,
            stt_model="whisper-large-v3"
        )

        # 2. Analyze image with transcription as query
        doctor_response = analyze_image_with_query(
            query=SYSTEM_PROMPT + "\nPatient says: " + transcription,
            encoded_image=encode_image(image_path),
            model=model
        )

        # 3. Generate TTS
        output_audio_path = "final_output.mp3"
        # We use gTTS by default as it's more reliable for free tier, 
        # but you can switch to elevenlabs if configured.
        text_to_speech_with_gtts(doctor_response, output_audio_path)

        return {
            "transcription": transcription,
            "response": doctor_response,
            "audio_url": "/api/audio_output"
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audio_output")
async def get_audio_output():
    return FileResponse("final_output.mp3", media_type="audio/mpeg")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root_check():
    return {"status": "healthy", "message": "AI Doctor 2.0 API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
