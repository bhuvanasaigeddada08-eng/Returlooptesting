@echo off
TITLE ReturnLoop LPU - Free Online Tunnel (Cloudflare)
color 0B
echo ===================================================
echo     ReturnLoop LPU - Free Public HTTPS Tunnel
echo ===================================================
echo.
echo Make sure START_SERVERS.bat is already running first!
echo.
echo Connecting Cloudflare Tunnel to http://localhost:5173 ...
echo.
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:5173
pause
