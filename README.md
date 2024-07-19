## Restful Server for Souq Aljomaa System

- To install the server first install python, then install MariaDB server and Redis server.
- Go to sever path and create virtus=al environment (`python -m venv .venv`).
- Activete the virtual environment (`.\.venv\Scripts\activate`).
- Install dependiceies (`pip install -r requirements.txt`).
- Run the server (`python app.py`). 
- Test the server (`python test.py`).
- Finally, install the serive as Windows service:
    `nssm install FlaskService python.exe "C:\path\to\flask_service.py"`