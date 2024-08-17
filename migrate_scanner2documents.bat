@echo off
setlocal enabledelayedexpansion

:: Prompt the user for database connection details
set /p DB_USER="Enter MySQL username (default: manassa): "
if "%DB_USER%"=="" set DB_USER=manassa

set /p DB_PASSWORD="Enter MySQL password: "

set /p DB_NAME="Enter database name (default: souq_aljomaa): "
if "%DB_NAME%"=="" set DB_NAME=souq_aljomaa

:: List of tables
set tables=Model1 Model2 Model3 Model4 Model5 Model6 Model7

:: Loop through each table and execute the SQL commands
for %%t in (%tables%) do (
    echo Updating table %%t...
    
    :: Rename the column from 'scanner' to 'documents'
    mysql -u %DB_USER% -p%DB_PASSWORD% -e "ALTER TABLE %DB_NAME%.%%t CHANGE COLUMN scanner documents TEXT;"
    
    :: Update the column values to JSON format
    mysql -u %DB_USER% -p%DB_PASSWORD% -e "UPDATE %DB_NAME%.%%t SET documents = CASE WHEN documents IS NOT NULL THEN CONCAT('[''"', REPLACE(documents, '"', '\"'), '"']') ELSE '[]' END;"
    
    echo Table %%t updated.
)

echo All tables have been updated.
pause
