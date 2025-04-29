@echo off
echo [⏳] Waiting 10 seconds before detaching RDP session...
timeout /t 10 /nobreak >nul

for /f "tokens=3" %%i in ('query session ^| findstr /i "rdp-tcp"') do (
    echo [✅] Detaching RDP session ID: %%i
    tscon %%i /dest:console
)

echo [✅] RDP detached. Closing...
exit
