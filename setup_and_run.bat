@echo off
setlocal
TITLE AI Doctor 2.0 - OneShot Venv Setup & Launch

echo ==================================================
echo   AI DOCTOR 2.0: SYNAPSE CLINICAL AI - VENV SETUP
echo ==================================================
echo.

:: 1. Initialize Virtual Environment
echo [1/5] Initializing Python virtual environment...
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
) else (
    echo [SUCCESS] Virtual environment already exists.
)

:: 2. Activate and Install
echo [2/5] Activating venv and installing dependencies...
call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b %errorlevel%
)
echo [SUCCESS] Environment ready.
echo.

:: 3. Frontend Setup
echo [3/5] Syncing Frontend dependencies (package.json)...
cd frontend
call npm install
cd ..
echo [SUCCESS] Frontend ready.
echo.

:: 4. Launch Services
echo [4/5] Launching Neural Backend (Port 8000)...
start "AI Doctor Backend" cmd /k "call .venv\Scripts\activate && python main.py"

echo Launching Synapse Dashbord (Port 5173)...
start "AI Doctor Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==================================================
echo   SERVICES LAUNCHED SUCCESSFULLY!
echo ==================================================
echo Backend: http://localhost:8000 (Venv: active)
echo Frontend: http://localhost:5173
echo.
echo You can now close this setup window.
echo ==================================================
pause
