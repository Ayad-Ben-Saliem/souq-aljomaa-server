## Restful Server for Souq Aljomaa System

- To install the server first install python, then install MariaDB server and Redis server.
- run `create_manassa_user.bat` to create database user.
- Go to sever path and create virtusal environment (`python -m venv .venv`).
- Activete the virtual environment (`.\.venv\Scripts\activate`).
- Install dependiceies (`pip install -r requirements.txt`).
- Run the server (`python app.py`).
- Test the server (`python test.py`).
- Finally, install the server as Windows service, open Command Prompt as Administrator and go to server path and run the following command:
  `service.bat`
