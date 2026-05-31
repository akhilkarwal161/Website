@echo off
:: =================================================================
:: Antigravity CLI Context Resume Script
:: =================================================================

echo [INFO] Resuming project context for "Website"...
cd /d "F:\REpo\Website"

:: Launch Antigravity CLI in the current directory
:: This ensures ANTIGRAVITY.md, README.md and project files are loaded
if exist "E:\CLI\agy.exe" (
    "E:\CLI\agy.exe"
) else (
    antigravity
)
