# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


if __name__ == "__main__":
    input_text="Hi this is Ai with Hassan!"
    text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable must be set before using the ElevenLabs client.")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "21m00Tcm4TlvDq8ikWAM",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice

import subprocess
import platform

def play_audio_file(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-NoProfile', '-Command', f'Start-Process -FilePath "{output_filepath}"'], check=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath], check=True)
        else:
            raise OSError("Unsupported operating system")
    except FileNotFoundError:
        print(f"Audio playback command not found on {os_name}; saved file to {output_filepath}")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    play_audio_file(output_filepath)


    # input_text="Hi this is Ai with Hassan, autoplay testing!"
    # text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set before using the ElevenLabs client.")
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    try:
        audio=client.generate(
            text= input_text,
            voice= "21m00Tcm4TlvDq8ikWAM",
            output_format= "mp3_22050_32",
            model= "eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
    except ApiError as e:
        error_body = getattr(e, 'body', {})
        if isinstance(error_body, dict) and error_body.get('detail', {}).get('code') == 'paid_plan_required':
            print("ElevenLabs voice requires a paid subscription. Falling back to gTTS.")
            text_to_speech_with_gtts(input_text=input_text, output_filepath=output_filepath)
            return output_filepath
        raise
    play_audio_file(output_filepath)

if __name__ == "__main__":
    # input_text="Hi this is Ai with Hassan, autoplay testing!"
    # text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
    pass