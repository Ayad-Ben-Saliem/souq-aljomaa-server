@echo off
setlocal enabledelayedexpansion

:: Prompt for MariaDB root username and password

set /p dbuser=Enter MariaDB root username (Default: root): 
if "%dbuser%"=="" set dbuser=root

set /p dbpass=Enter MariaDB root password: 

:: Check if the user 'manassa' exists
echo Checking if user 'manassa' exists...
echo exit | mariadb -u %dbuser% -p%dbpass% -e "SELECT User FROM mariadb.user WHERE User='manassa';" | findstr /i "manassa"
if !errorlevel! == 0 (
    echo User 'manassa' already exists.
) else (
    echo Creating user 'manassa'...
    mariadb -u %dbuser% -p%dbpass% -e "CREATE USER 'manassa'@'localhost' IDENTIFIED BY 'M@na55a.ly';"
)

:: Check if the database 'souq_aljomaa' exists
echo Checking if database 'souq_aljomaa' exists...
echo exit | mariadb -u %dbuser% -p%dbpass% -e "SHOW DATABASES LIKE 'souq_aljomaa';" | findstr /i "souq_aljomaa"
if !errorlevel! == 0 (
    echo Database 'souq_aljomaa' already exists.
) else (
    echo Creating database 'souq_aljomaa'...
    mariadb -u %dbuser% -p%dbpass% -e "CREATE DATABASE souq_aljomaa;"
)

:: Grant privileges to the user 'manassa'
echo Granting privileges to user 'manassa' on database 'souq_aljomaa'...
mariadb -u %dbuser% -p%dbpass% -e "GRANT ALL PRIVILEGES ON souq_aljomaa.* TO 'manassa'@'localhost';"
mariadb -u %dbuser% -p%dbpass% -e "FLUSH PRIVILEGES;"

echo All done!
pause
