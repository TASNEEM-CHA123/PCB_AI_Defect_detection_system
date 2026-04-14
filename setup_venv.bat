@echo off
echo ===================================================
echo   InspectAid: Project Environment Setup (Phase 2)
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [1/3] Creating Virtual Environment (venv)...
    python -m venv venv
) else (
    echo [1/3] Virtual Environment already exists. Skipping creation.
)

:: Activate and Install Requirements
echo [2/3] Activating environment and installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo [3/3] Setup Complete!
echo.
echo To start work, always run: venv\Scripts\activate.bat
echo Then run your app: streamlit run app.py
echo.
pause
