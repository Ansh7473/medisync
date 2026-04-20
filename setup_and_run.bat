@echo off
setlocal
TITLE AI Doctor 2.0 - OneShot Conda Setup & Launch

echo ==================================================
echo   AI DOCTOR 2.0: SYNAPSE CLINICAL AI - CONDA SETUP
echo ==================================================
echo.

:: 1. Initialize Conda
echo [1/5] Initializing Conda environment...
set CONDA_PATH=C:\Users\anshs\miniconda3
set ENV_NAME=medisync

if not exist "%CONDA_PATH%\Scripts\activate.bat" (
    echo [ERROR] Conda activation script not found at %CONDA_PATH%
    echo Please update the CONDA_PATH in this .bat file.
    pause
    exit /b 1
)

call "%CONDA_PATH%\Scripts\activate.bat" base

:: 2. Check/Create Environment
echo [2/5] Checking for '%ENV_NAME%' environment...
conda env list | findstr /C:"%ENV_NAME%" > nul
if %errorlevel% neq 0 (
    echo [INFO] '%ENV_NAME%' environment not found. Creating it...
    call conda create -n %ENV_NAME% python=3.10 -y
) else (
    echo [SUCCESS] '%ENV_NAME%' environment already exists.
)

:: 3. Activate and Install
echo [3/5] Activating '%ENV_NAME%' and installing dependencies...
call conda activate %ENV_NAME%
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b %errorlevel%
)
echo [SUCCESS] Environment ready.
echo.

:: 4. Frontend Setup
echo [4/5] Syncing Frontend dependencies (package.json)...
cd frontend
call npm install
cd ..
echo [SUCCESS] Frontend ready.
echo.

:: 5. Launch Services
echo [5/5] Launching Neural Backend (Port 8000)...
start "AI Doctor Backend (%ENV_NAME%)" cmd /k "call %CONDA_PATH%\Scripts\activate.bat %ENV_NAME% && python server.py"

echo Launching Synapse Dashbord (Port 5173)...
start "AI Doctor Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==================================================
echo   SERVICES LAUNCHED SUCCESSFULLY!
echo ==================================================
echo Backend: http://localhost:8000 (Conda: %ENV_NAME%)
echo Frontend: http://localhost:5173
echo.
echo You can now close this setup window.
echo ==================================================
pause
