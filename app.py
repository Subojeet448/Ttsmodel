import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from TTS.api import TTS
import uvicorn

app = FastAPI(title="TTS API")

# TTS initialize
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

if __name__ == "__main__":
    # Render ka PORT environment variable use karo
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
