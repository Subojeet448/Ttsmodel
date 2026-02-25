import os
import asyncio
import edge_tts
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="Edge TTS API")

# Output folder for audio files
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "Online", "engine": "Edge-TTS", "message": "Go to /say?text=hello"}

@app.get("/say")
async def say(text: str = Query(..., description="Text to convert to speech")):
    if not text:
        return JSONResponse({"status": "error", "message": "No text provided"}, status_code=400)

    output_file = os.path.join(OUTPUT_DIR, "output.mp3")
    
    # Voice options: en-US-GuyNeural, en-US-AriaNeural, hi-IN-MadhurNeural (Hindi)
    voice = "en-US-GuyNeural" 
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Returns the actual audio file so you can hear it in browser
        return FileResponse(output_file, media_type="audio/mpeg", filename="speech.mp3")
    
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
