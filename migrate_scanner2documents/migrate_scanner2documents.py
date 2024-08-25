import sqlite3
from sqlite3 import Cursor
import traceback
import datetime
import shutil
import os
import re


# Function to sanitize filenames
def sanitize_filename(filename):
    # Replace invalid characters with an underscore
    return re.sub(r'[\\/:*?"<>|]', '_', filename)


def copy_image(image_dir:str) -> str:
    if not image_dir.startswith("migrate_scanner2documents"):
        image_dir = os.path.join("migrate_scanner2documents", image_dir)
    
    if os.path.isfile(image_dir):        
        timestamp = datetime.datetime.now().isoformat()
        file_extension = os.path.splitext(image_dir)[-1]
        filename = fr"uploads\{timestamp}{file_extension}"
        
        filename = os.path.join("uploads", sanitize_filename(filename))
            
        shutil.copy2(image_dir, filename)
        
        return filename


def migrate(cursor: Cursor, table_name):
    try:
        cursor.execute(f"SELECT id, scanner FROM {table_name} WHERE scanner IS NOT NULL;")
        result = cursor.fetchall()
        print(f'{table_name}:', len(result))
        for row in result:
            id:int = row[0]
            scanner: str = row[1]
            image_dir = scanner.split('\\AppData\\Roaming\\com.example\\souq_aljomaa\\SouqAljomaa\\')[1]
            
            image_dir = copy_image(image_dir)
            
            if image_dir:
                # If image_dir not None
                cursor.execute(f'UPDATE {table_name} SET scanner = \'["{image_dir}"]\' WHERE id = {id};')
        cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN scanner TO documents;")
        
    except Exception as e:
        print(traceback.format_exc())
        


def main():
    try:
        connection = sqlite3.connect('migrate_scanner2documents/backup.db')
        cursor = connection.cursor()
        
        for table_name in ["Model1", "Model2", "Model3", "Model4", "Model5", "Model6", "Model7"]:
            migrate(cursor, table_name)

        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()