from flask import current_app, jsonify, url_for
import mysql.connector
import mysql.connector.cursor
from mysql.connector import pooling
from constants import *

import datetime
import hashlib
import json
import os
import re
from typing import Union
from functools import wraps

from werkzeug.datastructures.file_storage import FileStorage

class Database:

    pool: pooling.MySQLConnectionPool = None
    connection: pooling.PooledMySQLConnection = None
    cursor = None
    _dbconfig = {
        'user': "manassa",
        'host': "localhost",
        'password': "M@na55a.ly",
        'database': "souq_aljomaa"
    }

    def initialize_mysql_pool(self):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                **self._dbconfig
            )
        except mysql.connector.Error as err:
            print("Error creating pool:", err)


    def create_db_if_not_exist(self):
        try:
            connection = mysql.connector.connect(
                user = "manassa",
                host = "localhost",
                password = "M@na55a.ly",
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS souq_aljomaa")
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)
            return None


    def establish_mysql_connection(self):
        if self.pool is None:
            self.initialize_mysql_pool()
        else:
            if self.connection is not None and self.connection.is_connected():
                return self.connection;

        if self.pool is None: 
            return None

        try:
            self.connection = self.pool.get_connection()
            self.cursor = self.connection.cursor(dictionary=True)            
        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)

    
    def check_mysql_connection(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.connection or not self.connection.is_connected():
                print("MySQL is not connected. Trying to reconnect ...")
                self.initialize_mysql_connection()
                if not self.connection or not self.connection.is_connected():
                    return None
                
            return method(self, *args, **kwargs)
        return wrapper


    def initialize(self):
        self.create_db_if_not_exist()
        self.initialize_mysql_connection()


    def initialize_mysql_connection(self):
        if self.pool is None or self.connection is None or not self.connection.is_connected():
            self.establish_mysql_connection()

        if self.pool is not None and self.connection is not None and self.connection.is_connected():
            self.initialize_tabels()


    @check_mysql_connection
    def initialize_tabels(self):   
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                password TEXT NOT NULL,
                isAdmin BOOL DEFAULT FALSE,
                modelsModifier BOOL DEFAULT FALSE
            )
        ''')

        # Insert the admin user if the Users table has zero rows
        self.cursor.execute(f'''
            INSERT INTO Users (name, username, password, isAdmin, modelsModifier)
            SELECT 'Admin', 'admin', '{self._hash_password('1234')}', TRUE, TRUE
            WHERE (SELECT COUNT(*) FROM Users) = 0;
        ''');   

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model1 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                locality VARCHAR(255) NOT NULL,
                witness VARCHAR(255) NOT NULL,
                responsible VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                fatherName VARCHAR(255) NOT NULL,
                grandfatherName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                motherName VARCHAR(255) NOT NULL,
                identifierNo VARCHAR(255),
                nationalId VARCHAR(255) NOT NULL,
                testimony TEXT,
                date VARCHAR(255) NOT NULL
            )
        ''');

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model2 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                locality VARCHAR(255) NOT NULL,
                witness VARCHAR(255) NOT NULL,
                responsible VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                fatherName VARCHAR(255) NOT NULL,
                grandfatherName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                identifierNo VARCHAR(255),
                identifierFrom VARCHAR(255),
                nationalId VARCHAR(255) NOT NULL,
                testimony TEXT,
                date VARCHAR(255) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model3 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                locality VARCHAR(255) NOT NULL,
                witness VARCHAR(255) NOT NULL,
                responsible VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                fatherName VARCHAR(255) NOT NULL,
                grandfatherName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                identifierNo VARCHAR(255),
                identifierFrom VARCHAR(255),
                nationalId VARCHAR(255) NOT NULL,
                testimony TEXT,
                date VARCHAR(255) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model4 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                locality VARCHAR(255) NOT NULL,
                witness VARCHAR(255) NOT NULL,
                responsible VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                fatherName VARCHAR(255) NOT NULL,
                grandfatherName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                identifierNo VARCHAR(255),
                identifierFrom VARCHAR(255),
                nationalId VARCHAR(255) NOT NULL,
                testimony TEXT,
                date VARCHAR(255) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model5 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                locality VARCHAR(255) NOT NULL,
                witness VARCHAR(255) NOT NULL,
                responsible VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                fatherName VARCHAR(255) NOT NULL,
                grandfatherName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                motherName VARCHAR(255) NOT NULL,
                identifierNo VARCHAR(255),
                nationalId VARCHAR(255) NOT NULL,
                familyBookletNumber VARCHAR(255) NOT NULL,
                familyDocumentNumber VARCHAR(255) NOT NULL,
                issuePlace VARCHAR(255) NOT NULL,
                issueDate VARCHAR(255) NOT NULL,
                residence VARCHAR(255) NOT NULL,
                nearestPoint VARCHAR(255) NOT NULL,
                date VARCHAR(255) NOT NULL
            )
        ''');

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model6 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                ownerName VARCHAR(255) NOT NULL,
                ownerPhone VARCHAR(255) NOT NULL,
                tenantName VARCHAR(255) NOT NULL,
                tenantPhone VARCHAR(255) NOT NULL,
                streetCode VARCHAR(255) NOT NULL,
                shopNo VARCHAR(255) NOT NULL,
                businessType VARCHAR(255) NOT NULL,
                businessCategory VARCHAR(255) NOT NULL
            )
        ''');

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Model7 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                at VARCHAR(255) NOT NULL,
                documents TEXT,
                streetNo VARCHAR(255) NOT NULL,
                buildingNo VARCHAR(255) NOT NULL,
                registrationNo VARCHAR(255) NOT NULL,
                familyHeadName VARCHAR(255) NOT NULL,
                malesCount INTEGER NOT NULL,
                femalesCount INTEGER NOT NULL,
                widows TEXT,
                divorced TEXT,
                disabilities TEXT,
                lowIncome TEXT,
                unemployed TEXT,
                familyHeadDeathDate VARCHAR(255),
                currentFamilyHeadName VARCHAR(255),
                formFiller VARCHAR(255) NOT NULL,
                notes TEXT
            )
        ''')


    # Users related methods


    def _hash_password(self, password: str):
        hashed_password = hashlib.sha512(f'manassa{password}.ly'.encode())
        return hashed_password.hexdigest()


    @check_mysql_connection
    def login(self, username: str, password: str) -> Union[dict[str, any], None]:
        query = f"SELECT * FROM Users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, self._hash_password(password)))
        return self.cursor.fetchone()


    @check_mysql_connection
    def get_user(self, id: int) -> Union[dict[str, any], None]:
        query = f"SELECT * FROM Users WHERE id = %s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()
    

    @check_mysql_connection
    def get_user_by_username(self, username: str) -> Union[dict[str, any], None]:
        query = f"SELECT * FROM Users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()


    @check_mysql_connection
    def get_users(self, ids: list[int]) -> list[dict[str, any]]:
        query = 'SELECT * FROM Users'
        if ids:
            # Create a comma-separated list of placeholders
            placeholder_list = ', '.join(['%s'] * len(ids))
            query += f' WHERE id IN ({placeholder_list})'

        self.cursor.execute(query, tuple(ids if ids else []))
        return self.cursor.fetchall()


    @check_mysql_connection
    def save_user(self, data) -> Union[dict[str, any], None]:
        """Saves a new user record based on the provided data.
        Constructs the appropriate SQL query dynamically based on schema."""

        if 'id' in data:
            del data['id']

        data['password'] = self._hash_password(data['password'])

        # Construct the SQL query dynamically based on data
        keys = data.keys()
        values = data.values()
        parameters = ", ".join([key for key in keys])
        arguments = ('%s, ' * len(keys))[0 : -2]
        query = f'INSERT INTO Users ({parameters}) VALUES ({arguments})'

        try:
            # Execute the query with combined data
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            id = self.cursor.lastrowid
            
            # Return the saved model data
            return self.get_user(id)
        except mysql.connector.Error as err:
            print("Database error while saving user:", err)
            raise Exception(err.msg)


    @check_mysql_connection
    def update_user(self, id: int, data: dict[str, any]) -> Union[dict[str, any], None]:
        """Updates an existing model record based on the provided data."""

        if 'id' in data:
            if id != data['id']:
                raise 'id != data["id"]'
            del data['id']

        data['password'] = self._hash_password(data['password'])

        # Construct the SQL query dynamically based on data
        keys = data.keys()
        values = data.values()

        parameters = ", ".join([f'{key} = %s' for key in keys])
        query = f'UPDATE Users SET {parameters} WHERE id = {id}'

        try:
            # Execute the query with combined data
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            
            # Return the saved model data
            return self.get_user(id)
        except mysql.connector.Error as err:
            print("Database error while updating user:", err)
            raise Exception(err.msg)


    @check_mysql_connection
    def delete_user(self, id):
        """Deletes an existing model record based on its ID."""

        query = f'DELETE FROM Users WHERE id = {id}'

        try:
            # Execute the delete query
            self.cursor.execute(query)
            self.connection.commit()

            if self.cursor.rowcount > 0:
                # Model deleted successfully
                return jsonify({'message': 'User deleted successfully'})
            else:
                return jsonify({"error": USER_NOT_FOUND}), 404  # User not found
        except mysql.connector.Error as err:
            print("Database error while deleting user:", err)
            return jsonify({"error": ERROR_DELETE_USER}), 500


    # Models related methods


    @check_mysql_connection
    def get_model(self, model_type: str, id: int) -> Union[dict[str, any], None]:
        query = f"SELECT * FROM {model_type} WHERE id = %s"
        self.cursor.execute(query, (id,))
        model = self.cursor.fetchone()
        if model:
            self._resolve_model_documents(model)
        return model
        

    @check_mysql_connection
    def get_models(self, model_type: str, ids: list[int]) -> list[dict[str, any]]:
        query = f"SELECT * FROM {model_type}"
        if ids:
            # Create a comma-separated list of placeholders
            placeholder_list = ', '.join(['%s'] * len(ids))
            query += f' WHERE id IN ({placeholder_list})'

        self.cursor.execute(query, tuple(ids if ids else []))
        models = self.cursor.fetchall()
        self._resolve_models_documents(models)
        return models
        

    def _where_query(self, fields_name: list[str], search_text: str, model_title: str) -> str:
        if not fields_name or not search_text: return ''

        fields_name.append(model_title)
        
        result = 'WHERE '
        for txt in search_text.split(' '):
            result += '(';
            for field_name in fields_name:
                result += f'{field_name} LIKE "%{txt}%" OR ';
            result = result[0: len(result) - 4];
            result += ') AND ';
        

        result = result[0: len(result) - 5];
        return result;

    
    def split_ids(self, result) -> dict[str, list[int]]:
        """
        Splits IDs from a database query result into a dictionary with table names as keys and lists of IDs as values.

        Args:
            result: A database query result object (replace with your specific type)

        Returns:
            A dictionary with table names as keys and lists of IDs as values.
        """

        table_names = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7']
        ids = {}

        for row in result:
            table_name = row.get('table_name')  # Use .get() for safer key access
            if table_name and table_name in table_names:  # Check if table_name exists and is valid
                ids.setdefault(table_name, []).append(row.get('id'))  # Use setdefault for efficient dictionary creation

        return ids


    @check_mysql_connection
    def search(self, limit = 10, offset = 0, text = None) -> dict[str, list[dict[str, any]]] :
        if text == None: return {}

        if not limit: limit = 10
        if offset is None: offset = 0

        model1_title = '"إفادة بعدم الزواج بغير ليبية"'
        model2_title = '"إفادة بعدم ملكية مسكن"'
        model3_title = '"إفادة بحسن السيرة والسلوك"'
        model4_title = '"إفادة بشأن واقعة"'
        model5_title = '"إفادة بالإقامة"'
        model6_title = '"كشف بحصر الأنشطة التجارية"'
        model7_title = '"نموذج حصر العائلات الليبية"'

        model1_fields = [
            'locality',
            'witness',
            'responsible',
            'firstName',
            'fatherName',
            'grandfatherName',
            'lastName',
            'motherName',
            'identifierNo',
            'nationalId',
            'testimony',
        ];
        model234_fields = [
            'locality',
            'witness',
            'responsible',
            'firstName',
            'fatherName',
            'grandfatherName',
            'lastName',
            'identifierNo',
            'identifierFrom',
            'nationalId',
            'testimony',
        ];
        model5_fields = [
            'locality',
            'witness',
            'responsible',
            'firstName',
            'fatherName',
            'grandfatherName',
            'lastName',
            'motherName',
            'identifierNo',
            'nationalId',
            'familyBookletNumber',
            'familyDocumentNumber',
            'issuePlace',
            'issueDate',
            'residence',
            'nearestPoint',
        ];
        model6_fields = [
            'ownerName',
            'ownerPhone',
            'tenantName',
            'tenantPhone',
            'streetCode',
            'shopNo',
            'businessType',
            'businessCategory',
        ];
        model7_fields = [
            'streetNo',
            'buildingNo',
            'registrationNo',
            'familyHeadName',
            'malesCount',
            'femalesCount',
            'widows',
            'divorced',
            'disabilities',
            'lowIncome',
            'unemployed',
            'familyHeadDeathDate',
            'currentFamilyHeadName',
            'formFiller',
            'notes',
        ];

        query = f'''
            SELECT id, at, table_name
            FROM (
                SELECT id, at, 'Model1' AS table_name FROM Model1
                {self._where_query(model1_fields, text, model1_title)}
                UNION ALL
                SELECT id, at, 'Model2' AS table_name FROM Model2
                {self._where_query(model234_fields, text, model2_title)}
                UNION ALL
                SELECT id, at, 'Model3' AS table_name FROM Model3
                {self._where_query(model234_fields, text, model3_title)}
                UNION ALL
                SELECT id, at, 'Model4' AS table_name FROM Model4
                {self._where_query(model234_fields, text, model4_title)}
                UNION ALL
                SELECT id, at, 'Model5' AS table_name FROM Model5
                {self._where_query(model5_fields, text, model5_title)}
                UNION ALL
                SELECT id, at, 'Model6' AS table_name FROM Model6
                {self._where_query(model6_fields, text, model6_title)}
                UNION ALL
                SELECT id, at, 'Model7' AS table_name FROM Model7
                {self._where_query(model7_fields, text, model7_title)}
            ) AS combined_data
            ORDER BY at DESC
            LIMIT {limit} OFFSET {offset}
        '''

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            models_ids = self.split_ids(result);
            all_models = {}
            for model_type, model_ids in models_ids.items():
                all_models[model_type] = self.get_models(model_type, model_ids)

            return all_models


    def _resolve_models_documents(self, models: list[dict[str, any]]) -> list[dict[str, any]]:
        for model in models:
            self._resolve_model_documents(model)
        return models


    def _resolve_model_documents(self, model: dict[str, any]) -> dict[str, any]:
        if isinstance(model['documents'], str):
            model['documents'] = json.loads(model['documents'])

        # model['documents'] = self._documents_name2url(model['documents'])
        return model
    

    def _documents_name2url(self, documents: list[str]) -> dict[str, any]:
        result = []
        for doc in documents:
            # Generate the URL for the uploaded image
            image_url = self._get_document_url(doc)
            result.append(image_url)
        return result



    # Function to sanitize filenames
    def sanitize_filename(self, filename):
        # Replace invalid characters with an underscore
        return re.sub(r'[\\/:*?"<>|]', '_', filename)

    
    def _get_document_url(self, filename: str):
        with current_app.app_context():
            image_url = url_for('file', filename=filename, _external=True)
        return image_url
    

    def _is_document_exists(self, filename: str) -> bool:
        return os.path.exists(UPLOAD_FOLDER + filename)

    def _save_documents(self, files: list[FileStorage]) -> list[str]:
        result: list[str] = []
        for file in files:
            if file:
                timestamp = datetime.datetime.now().isoformat()
                file_extension = os.path.splitext(file.filename)[-1]
                filename = f"{timestamp}{file_extension}"
                filename = self.sanitize_filename(filename)
                
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                
                result.append(filename)
        return result


    def _delete_document(self, filename) -> bool:
        if os.path.exists(filename):
            return os.remove(filename) is None
            
        filename = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filename):
            return os.remove(filename) is None
        
        return False


    @check_mysql_connection
    def save_model(self, model_type, data, files: list[FileStorage]) -> Union[dict[str, any], None]:
        """Saves a new model record based on the provided data and model type.
        Constructs the appropriate SQL query dynamically based on model schema."""

        if model_type not in ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7']:
            return jsonify({"error": INVALID_TYPE}), 400

        if 'id' in data:
            del data['id']

        # Update `at` with current timestamp
        data['at'] = datetime.datetime.now().isoformat()

        docs = self._save_documents(files);
        data['documents'] = json.dumps(docs)

        # Construct the SQL query dynamically based on data
        keys = data.keys()
        values = data.values()

        parameters = ", ".join([key for key in keys])
        arguments = ('%s, ' * len(keys))[0 : -2]
        
        query = f'INSERT INTO {model_type} ({parameters}) VALUES ({arguments})'

        # Execute the query with combined data
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        model_id = self.cursor.lastrowid
        
        # Return the saved model data
        return self.get_model(model_type, model_id)


    @check_mysql_connection
    def update_model(self, id: int, model_type: str, data: dict[str, any], files: list[FileStorage]) -> Union[dict[str, any], None]:
        """Updates an existing model record based on the provided data."""

        if model_type not in ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7']:
            return jsonify({"error": self.INVALID_TYPE}), 400

        if 'id' in data:
            if id != data['id']:
                raise 'id != data["id"]'
            del data['id']

        # Update `at` with current timestamp
        data['at'] = datetime.datetime.now().isoformat()

        # Construct the SQL query dynamically based on data
        keys = data.keys()
        values = data.values()

        docs = data['documents']
        if isinstance(docs, str): docs = json.loads(docs)

        # Get only documens existed in uplaods folder
        documents = []
        for doc in docs:
            if self._is_document_exists(doc): documents.append(doc)

        documents.extend(self._save_documents(files))
        data['documents'] = json.dumps(documents)

        exiting_model = self.get_model(model_type, id)
        for doc in exiting_model['documents']:
            if doc not in documents:
                self._delete_document(doc)

        parameters = ", ".join([f'{key} = %s' for key in keys])

        query = f'UPDATE {model_type} SET {parameters} WHERE id = {id}'

        # Execute the query with combined data
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        
        # Return the saved model data
        return self.get_model(model_type, id)


    @check_mysql_connection
    def delete_model(self, model_type: str, id: int):
        """Deletes an existing model record based on its ID."""

        if model_type not in ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7']:
            return jsonify({"error": INVALID_TYPE}), 400
        
        exiting_model = self.get_model(model_type, id)
        for doc in exiting_model['documents']:
            self._delete_document(doc)

        query = f'DELETE FROM {model_type} WHERE id = {id}'

        try:
            # Execute the delete query
            self.cursor.execute(query)
            self.connection.commit()

            if self.cursor.rowcount > 0:
                # Model deleted successfully
                return jsonify({'message': 'Model deleted successfully'})
            else:
                return jsonify({"error": MODEL_NOT_FOUND}), 404  # Model not found
        except mysql.connector.Error as err:
            print("Database error while deleting model:", err)
            return jsonify({"error": ERROR_DELETE_MODEL}), 500


    def create_new_zip_backup(self, password=None):
        import os
        import pyzipper

        backup = 'backup.zip'
        database = 'database.db'
        uploads = 'uploads\\'

        # Remove existing backup file if it exists
        if os.path.exists(backup):
            os.remove(backup)
            
        # Create a new database backup
        self.create_new_database_backup()

        if password:
            zipf = pyzipper.AESZipFile(backup, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
            zipf.setpassword(password.encode('utf-8'))
        else:
            zipf = pyzipper.ZipFile(backup, 'w', compression=pyzipper.ZIP_DEFLATED)
            
        # Add the single database file to the ZIP archive
        zipf.write(database, os.path.basename(database))
        
        # Walk through the directory and add each file
        for root, _, files in os.walk(uploads):
            for file in files:
                file_path = os.path.join(root, file)
                # Compute the relative path of the file within the folder
                relative_path = os.path.relpath(file_path, uploads)
                # Create a path for the file within the 'uploads' folder in the ZIP archive
                arcname = os.path.join('uploads', relative_path)
                # Add file to the ZIP archive
                zipf.write(file_path, arcname)
        
        zipf.close()



    @check_mysql_connection
    def create_new_database_backup(self):
        import sqlite3
        import pandas as pd

        database = 'database.db'

        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        if os.path.exists(database):
            os.remove(database)

        sqlite_conn = sqlite3.connect(database)

        for table in tables:
            table_name = table['Tables_in_souq_aljomaa']

            # Read the MySQL table into a pandas DataFrame
            df = pd.read_sql(f"SELECT * FROM {table_name}", self.connection)

            # Write the DataFrame to a SQLite table
            df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)

        sqlite_conn.commit()
        sqlite_conn.close()
