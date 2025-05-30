@echo off

set PYTHON_VERSION=3.10

echo [*] Creating virtual environment via uv (Python %PYTHON_VERSION%)...
uv venv --python python%PYTHON_VERSION%

echo [*] Installing dependencies...
uv pip install -r requirements.txt

echo [x] Setup complete.
