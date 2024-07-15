@echo off

nssm-2.24\win64\nssm.exe install "Souq Aljomaa Service" C:\Users\HP\VSCodeProjects\souq-aljomaa-server\start_flask_app.bat
nssm-2.24\win64\nssm.exe set "Souq Aljomaa Service" AppStdout C:\Users\HP\VSCodeProjects\souq-aljomaa-server\service_output.log
nssm-2.24\win64\nssm.exe set "Souq Aljomaa Service" AppStderr C:\Users\HP\VSCodeProjects\souq-aljomaa-server\service_error.log
nssm-2.24\win64\nssm.exe start "Souq Aljomaa Service"