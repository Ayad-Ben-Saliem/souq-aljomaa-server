import sqlite3
import mysql.connector
from mysql.connector import Error

# Function to read data from SQLite and insert into MySQL
def migrate_sqlite_to_mysql(sqlite_db, mysql_conn):
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_db)
        cursor = sqlite_conn.cursor()
        
        tables = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7']
        for table_name in tables:
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
        
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns][1:]
            column_placeholders = ', '.join(['%s'] * len(column_names))
            column_names_str = ', '.join(column_names)

            # Insert data into MySQL
            mysql_cursor = mysql_conn.cursor()
            insert_query = f"INSERT INTO {table_name} ({column_names_str}) VALUES ({column_placeholders})"
            for row in rows:
                row = row[1:]
                if table_name == 'Model7':
                    print('------------------------')
                    print(insert_query)
                    print()
                    for i in range(len(row)):
                        print(column_names[i], '=', row[i])
                    print('------------------------')
    
                mysql_cursor.execute(insert_query, row)
            mysql_conn.commit()
        
        cursor.close()
        sqlite_conn.close()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if (sqlite_conn):
            sqlite_conn.close()



mysql_conn = None
# Connect to MySQL
try:
    mysql_conn = mysql.connector.connect(
        host='localhost',
        database='souq_aljomaa',
        user='manassa',
        password='M@na55a.ly'
    )
    if mysql_conn.is_connected():
        print("Connected to MySQL database")
        
        # Migrate data from SQLite databases to MySQL
        migrate_sqlite_to_mysql('migrate_scanner2documents\\backup.db', mysql_conn)
        
except Error as e:
    print(f"Error: {e}")
finally:
    if (mysql_conn is not None and mysql_conn.is_connected()):
        mysql_conn.close()
        print("MySQL connection is closed")
