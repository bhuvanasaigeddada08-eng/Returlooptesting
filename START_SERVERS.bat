@echo off
TITLE ReturnLoop LPU - Server Launcher
color 0A
echo ===================================================
echo       ReturnLoop LPU - Starting Full Application
echo ===================================================
echo.

set CURRENT_DIR=%~dp0
cd /d "%CURRENT_DIR%"

:: Determine Python Environment
set PYTHON_EXE=
if exist "%CURRENT_DIR%backend_venv\Scripts\python.exe" (
    set PYTHON_EXE=%CURRENT_DIR%backend_venv\Scripts\python.exe
    set BACKEND_DIR=%CURRENT_DIR%backend
) else if exist "%CURRENT_DIR%..\ReturnLoop\backend_venv\Scripts\python.exe" (
    set PYTHON_EXE=%CURRENT_DIR%..\ReturnLoop\backend_venv\Scripts\python.exe
    set BACKEND_DIR=%CURRENT_DIR%..\ReturnLoop\backend
) else (
    set PYTHON_EXE=python
    set BACKEND_DIR=%CURRENT_DIR%backend
)

:: Determine Frontend Directory
set FRONTEND_DIR=
if exist "%CURRENT_DIR%frontend\node_modules" (
    set FRONTEND_DIR=%CURRENT_DIR%frontend
) else if exist "%CURRENT_DIR%..\ReturnLoop\frontend\node_modules" (
    set FRONTEND_DIR=%CURRENT_DIR%..\ReturnLoop\frontend
) else (
    set FRONTEND_DIR=%CURRENT_DIR%frontend
)

:: Release any existing processes on 5000 and 5173
echo Cleaning up previous port bindings...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr /r ":5000[^0-9]"') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr /r ":5173[^0-9]"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [1/2] Starting Python Flask Backend on http://127.0.0.1:5000 ...
start "ReturnLoop Backend (Flask :5000)" cmd /k "cd /d ""%BACKEND_DIR%"" && ""%PYTHON_EXE%"" run.py"

echo Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
start "ReturnLoop Frontend (Vite :5173)" cmd /k "cd /d ""%FRONTEND_DIR%"" && npm run dev"

echo Waiting 3 seconds for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ===================================================
echo           ReturnLoop is now running!
echo ===================================================
echo.
echo - On this Laptop:
echo   Open: http://localhost:5173
echo.
echo - On your Mobile Phone (Same Wi-Fi):
echo   Open: http://172.22.81.254:5173
echo.
echo Admin Login Credentials:
echo   Email:    bhuvanasaigeddada3@gmail.com
echo   Password: Bitsat@26
echo.
echo Demo Accounts:
echo   Admin:   admin@returnloop.lpu.in  (or click 'Fill Admin Demo')
echo   Student: aarav.sharma@lpu.in      (or click 'Fill Student Demo')
echo ===================================================
echo.

start http://localhost:5173
pause
