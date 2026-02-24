import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from TTS.api import TTS  # Make sure TTS package installed

app = FastAPI(title="TTS API")

# Initialize TTS model once
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
except Exception as e:
    print("Error loading TTS model:", e)
    tts = None

@app.get("/")
def home():
    return {"status": "TTS API is running"}

@app.get("/say")
def say(text: str):
    if not tts:
        raise HTTPException(status_code=500, detail="TTS model not loaded")
    if not text:
        raise HTTPException(status_code=400, detail="Text query required")
    
    output_file = "output.wav"
    tts.tts_to_file(text=text, file_path=output_file)
    return JSONResponse({"status": "success", "file": output_file})
