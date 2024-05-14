#!/bin/bash

# Function to handle Ctrl+C and cleanup
cleanup() {
    echo "Stopping the servers..."
    kill "$frontend_pid" "$backend_pid"
    wait "$frontend_pid" "$backend_pid"
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

if command -v python &> /dev/null
then
    echo "Starting EntryPoint site server on port 8080: http://localhost:8080/posts.html"
    python -m http.server 8080 -d frontend &
    frontend_pid=$!
    pip install flask
    python backend/api.py &
    backend_pid=$!

    open "http://localhost:8080/posts.html" 2>/dev/null
elif command -v python3 &> /dev/null
then
    echo "Starting EntryPoint site server on port 8080: http://localhost:8080/posts.html"
    python3 -m http.server 8080 -d frontend &
    frontend_pid=$!
    pip3 install flask
    python3 backend/api.py &
    backend_pid=$!

    open "http://localhost:8080/posts.html" 2>/dev/null
else
    echo "Neither python nor python3 is installed."
fi

# Wait for background processes
wait "$frontend_pid" "$backend_pid"
