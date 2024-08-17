#!/bin/bash

# Prompt the user for database connection details
read -p "Enter MySQL username (default: manassa): " DB_USER
DB_USER=${DB_USER:-manassa}

read -sp "Enter MySQL password: " DB_PASSWORD
echo
read -p "Enter database name (default: souq_aljomaa): " DB_NAME
DB_NAME=${DB_NAME:-souq_aljomaa}

# List of tables
tables=("Model1" "Model2" "Model3" "Model4" "Model5" "Model6" "Model7")

# Loop through each table and execute the SQL commands
for table in "${tables[@]}"; do
    echo "Updating table $table..."
    
    # Rename the column from 'scanner' to 'documents'
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "ALTER TABLE $DB_NAME.$table CHANGE COLUMN scanner documents TEXT;"
    
    # Update the column values to JSON format
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "UPDATE $DB_NAME.$table SET documents = CASE WHEN documents IS NOT NULL THEN CONCAT('[\"', REPLACE(documents, '\"', '\\\"'), '\"]') ELSE '[]' END;"
    
    echo "Table $table updated."
done

echo "All tables have been updated."
