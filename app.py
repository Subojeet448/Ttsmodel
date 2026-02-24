import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from TTS.api import TTS

PORT = int(os.environ.get("PORT", 10000))  # Render port
app = FastAPI(title="TTS API")

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

@app.get("/")
def home():
    return {"status": "TTS API running"}

@app.get("/say")
def say(text: str):
    if not text:
        return JSONResponse({"status": "error", "message": "No text provided"}, status_code=400)
    output_file = "output.wav"
    tts.tts_to_file(text=text, file_path=output_file)
    return {"status": "success", "file": output_file}
