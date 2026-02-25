import os
import asyncio
import edge_tts
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="Multi-Voice TTS API")

# Output folder
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice List
VOICES = {
    "female": "en-US-AriaNeural",
    "male": "en-US-GuyNeural",
    "hindi_female": "hi-IN-SwaraNeural",
    "hindi_male": "hi-IN-MadhurNeural"
}

@app.get("/")
def home():
    # Ye main link hai jise aap Uptime Robot mein dalenge
    return {
        "status": "Online", 
        "uptime_robot": "Active",
        "available_voices": list(VOICES.keys()),
        "example": "/say?text=Hello&voice=female"
    }

@app.get("/ping")
def ping():
    """Uptime Robot ke liye chota endpoint"""
    return {"message": "pong", "status": "alive"}

@app.get("/say")
async def say(
    text: str = Query(..., description="Text to convert"), 
    voice: str = Query("female", description="Choose: female, male, hindi_female, hindi_male")
):
    if not text:
        return JSONResponse({"status": "error", "message": "No text provided"}, status_code=400)

    selected_voice = VOICES.get(voice.lower(), VOICES["female"])
    output_file = os.path.join(OUTPUT_DIR, "speech.mp3")
    
    try:
        communicate = edge_tts.Communicate(text, selected_voice)
        await communicate.save(output_file)
        return FileResponse(output_file, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
