#!/bin/bash
# Make sure script is executable: chmod +x start.sh

echo "Starting FastAPI server..."
# Use Render's PORT environment variable
uvicorn app:app --host 0.0.0.0 --port $PORT
