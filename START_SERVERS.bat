@echo off
TITLE ReturnLoop LPU - Server Launcher
color 0A
echo ===================================================
echo       ReturnLoop LPU - Starting Full Application
echo ===================================================
echo.

set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo [1/2] Starting Python Flask Backend on http://127.0.0.1:5000 ...
start "ReturnLoop Backend (Flask :5000)" cmd /k "cd /d ""%PROJECT_DIR%backend"" && ""%PROJECT_DIR%backend_venv\Scripts\python.exe"" run.py"

echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
start "ReturnLoop Frontend (Vite :5173)" cmd /k "cd /d ""%PROJECT_DIR%frontend"" && npm run dev"

echo Waiting 4 seconds for frontend to start...
timeout /t 4 /nobreak >nul

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
echo Login Credentials:
echo   Email:    bhuvanasaigeddada3@gmail.com
echo   Password: Bitsat@25
echo.
echo Demo Accounts:
echo   Admin:   admin@returnloop.lpu.in  (or click 'Fill Admin Demo')
echo   Student: aarav.sharma@lpu.in      (or click 'Fill Student Demo')
echo ===================================================
echo.

start http://localhost:5173
pause
