#!/bin/bash
# Make sure the file has execute permission: chmod +x start.sh

# Run FastAPI app using Render's PORT
uvicorn app:app --host 0.0.0.0 --port $PORT
