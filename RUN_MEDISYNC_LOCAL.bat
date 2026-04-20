@echo off
setlocal
TITLE MEDISYNC AI DOCTOR - LOCAL LAUNCHER

echo ==================================================
echo   MEDISYNC AI DOCTOR: PROFESSIONAL LOCAL LAUNCHER
echo ==================================================
echo.

:: 1. Verify Environment
echo [1/3] Checking virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment (.venv) not found.
    echo Please run setup_and_run.bat first.
    pause
    exit /b 1
)

:: 2. Check for Groq API Key
if "%GROQ_API_KEY%"=="" (
    echo [WARNING] GROQ_API_KEY is not set in your system environment.
    echo Make sure you have a .env file or set it manually.
)

:: 3. Start Backend
echo [2/3] Launching Neural Backend (Port 8000)...
start "Medisync Backend" cmd /k "call .venv\Scripts\activate && python main.py"

:: 4. Start Frontend
echo [3/3] Launching Synapse Dashboard (Port 5173)...
start "Medisync Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==================================================
echo   ALL SERVICES ARE STARTING!
echo ==================================================
echo.
echo   BACKEND:  http://localhost:8000
echo   FRONTEND: http://localhost:5173
echo.
echo   Note: If this is your first time, make sure you ran
echo   setup_and_run.bat first to install dependencies.
echo ==================================================
echo.
pause
