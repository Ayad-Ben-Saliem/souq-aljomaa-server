@echo off

set CURRENT_DIR=%~dp0

call "%CURRENT_DIR%.venv\Scripts\activate.bat"
python "%CURRENT_DIR%app.py"