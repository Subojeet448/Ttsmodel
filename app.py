from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid
import os

app = FastAPI()

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.get("/")
def home():
    return {"status": "TTS API running"}

@app.post("/tts")
async def generate_tts(text: str = Form(...)):
    file_path = f"voice_{uuid.uuid4().hex}.wav"
    tts.tts_to_file(text=text, file_path=file_path)
    return FileResponse(file_path, media_type="audio/wav")
