@echo off

set CURRENT_DIR=%~dp0

nssm-2.24\win64\nssm.exe install "Souq Aljomaa Service" "%CURRENT_DIR%start_flask_app.bat"
nssm-2.24\win64\nssm.exe set "Souq Aljomaa Service" AppStdout "%CURRENT_DIR%service_output.log"
nssm-2.24\win64\nssm.exe set "Souq Aljomaa Service" AppStderr "%CURRENT_DIR%service_error.log"
nssm-2.24\win64\nssm.exe set "Souq Aljomaa Service" DependOnService "MariaDB"  # Ensure "MariaDB" is the correct service name
nssm-2.24\win64\nssm.exe start "Souq Aljomaa Service"