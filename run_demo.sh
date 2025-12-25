#!/bin/bash
# Start the backend and frontend for the Vision Accessibility Demo

# Trap SIGINT to kill background processes
trap "kill 0" EXIT

echo "Starting Backend Server..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/vademos/server.py &

echo "Starting Dashboard..."
cd dashboard
npm run dev
