#!/bin/bash

if command -v python &> /dev/null
then
    echo "Starting EntryPoint site server on port 8080: http://localhost:8080/frontend/posts.html"
    python -m http.server 8080
elif command -v python3 &> /dev/null
then
    echo "Starting EntryPoint site server on port 8080: http://localhost:8080/frontend/posts.html"
    python3 -m http.server 8080
else
    echo "Neither python nor python3 is installed."
fi
