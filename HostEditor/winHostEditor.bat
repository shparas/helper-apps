@echo off
if "%1" NEQ "am_admin" (
	powershell start -verb runas '%0' am_admin & exit /b
)
cd /d "%~dp0"
type hosts.txt > C:\Windows\System32\drivers\etc\hosts
exit /b