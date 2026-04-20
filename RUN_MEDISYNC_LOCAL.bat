@echo off
setlocal
TITLE MEDISYNC AI DOCTOR - LOCAL LAUNCHER

echo ==================================================
echo   MEDISYNC AI DOCTOR: PROFESSIONAL LOCAL LAUNCHER
echo ==================================================
echo.

:: 1. Configuration
set CONDA_PATH=C:\Users\anshs\miniconda3
set ENV_NAME=medisync

:: 2. Verify Environment
echo [1/3] Initializing Conda and checking environment...
if not exist "%CONDA_PATH%\Scripts\activate.bat" (
    echo [ERROR] Conda not found at %CONDA_PATH%
    echo Please ensure Miniconda is installed.
    pause
    exit /b 1
)

:: 3. Check for Groq API Key
if "%GROQ_API_KEY%"=="" (
    echo [WARNING] GROQ_API_KEY is not set in your system environment.
    echo Make sure you have a .env file or set it manually.
)

:: 4. Start Backend
echo [2/3] Launching Neural Backend (Port 8000)...
start "Medisync Backend" cmd /k "call ^"%CONDA_PATH%\Scripts\activate.bat^" %ENV_NAME% && python main.py"

:: 5. Start Frontend
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
