#!/bin/bash

# Create executable for pdf2cbz

# Create executable
pyinstaller --onefile pdf2cbz.py

# Move executable to bin
mv dist/pdf2cbz pdf2cbz

# Remove build and dist directories
rm -rf build dist