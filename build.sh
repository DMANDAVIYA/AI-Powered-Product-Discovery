#!/usr/bin/env bash
# Build script for Render

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating chroma_db directory..."
mkdir -p chroma_db

echo "Build complete!"
