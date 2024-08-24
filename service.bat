@echo off
setlocal

:: Define variables
set CURRENT_DIR=%~dp0
set SERVICE_NAME=Souq Aljomaa Service
set SERVICE_EXEC="%CURRENT_DIR%start_flask_app.bat"
set LOG_STDOUT="%CURRENT_DIR%service_output.log"
set LOG_STDERR="%CURRENT_DIR%service_error.log"
set DEPENDENCY_SERVICE=MariaDB

:: Install the service
nssm-2.24\win64\nssm.exe install "%SERVICE_NAME%" %SERVICE_EXEC%

:: Set output and error log paths
nssm-2.24\win64\nssm.exe set "%SERVICE_NAME%" AppStdout %LOG_STDOUT%
nssm-2.24\win64\nssm.exe set "%SERVICE_NAME%" AppStderr %LOG_STDERR%

:: Attempt to set the dependency
echo Setting service dependency...
nssm-2.24\win64\nssm.exe set "%SERVICE_NAME%" DependOnService "%DEPENDENCY_SERVICE%"

:: Verify if dependency was set correctly
echo Checking if service dependency was set...
sc qc "%SERVICE_NAME%"

:: Start the service
nssm-2.24\win64\nssm.exe start "%SERVICE_NAME%"

:: Provide instructions for manual dependency configuration if needed
echo.
echo If you encounter issues with the dependency setting, please manually configure it using the following steps:
echo 1. Open `services.msc`.
echo 2. Find and open properties for "%SERVICE_NAME%".
echo 3. Go to the `Dependencies` tab and add "%DEPENDENCY_SERVICE%".
echo.
echo Alternatively, you can manually set the dependency using the following command:
echo sc config "%SERVICE_NAME%" depend= "%DEPENDENCY_SERVICE%"

endlocal
pause
