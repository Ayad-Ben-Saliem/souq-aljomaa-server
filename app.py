from datetime import timedelta
from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jti
from flask_redis import FlaskRedis
from db import Database
from constants import *
from waitress import serve


def create_app():
    app = Flask(__name__)

    # Configure your application to use a secret key for signing JWTs
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Token expiry time
    app.config['REDIS_URL'] = "redis://localhost:6379/0"

    return app

# Initialize Flask app
app = create_app()
jwt = JWTManager(app)
redis_store = FlaskRedis(app)

db = Database()


# Auth API endpoints
@app.route('/login', methods=['POST'])
def login():
    """Login with username and password."""
    username = request.json.get('username')
    password = request.json.get('password')

    user = db.login(username, password)
    if user:
        access_token = create_access_token(identity=username)
        jti = get_jti(access_token)
        redis_store.set(jti, 'true', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES'])

        return jsonify(access_token=access_token, current_user=user)
    return jsonify({"error": LOGIN_FAIL}), 404

@app.route('/auto_login', methods=['POST'])
@jwt_required()
def auto_login():
    """Relogin using access_token."""
    print('auto_login')
    username = get_jwt_identity()
    user = db.get_user_by_username(username)
    # user = None
    if user:
        access_token = create_access_token(identity=username)
        jti = get_jti(access_token)
        redis_store.set(jti, 'true', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES'])

        return jsonify(access_token=access_token, current_user=user)
    return jsonify({"error": LOGIN_FAIL}), 404


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jti(request.headers.get('Authorization').split()[1])
    redis_store.delete(jti)
    return jsonify(msg="Successfully logged out"), 200


# Token check blacklist loader
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = redis_store.get(jti)
    return token_in_redis is None




# Users API endpoints
@app.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    """Retrieves a specific user data by its ID."""
    user = db.get_user(id)
    if user:
        return jsonify(user)
    return jsonify({"error": USER_NOT_FOUND}), 404


@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """Retrieves all users data specified in ids"
    (get all users if empty or None)."""
    ids = request.json.get('ids')
    result = db.get_users(ids)
    return jsonify(result)
    

@app.route("/users", methods=["POST"])
@jwt_required()
def create_user():
    """Creates a new user record based on the provided data."""
    data = request.json
    if not data:
        return jsonify({"error": MISSING_DATA}), 400
    try:
        result = db.save_user(data)
        if result:
            return jsonify(result), 201
        return jsonify({"error": ERROR_SAVE_USER}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    """Updates an existing user record based on the provided data."""
    data = request.json
    if not data:
        return jsonify({"error": MISSING_DATA}), 400

    try:
        user = db.update_user(id, data)
        if user:
            if user.get('username') ==  get_jwt_identity():
                jti = get_jti(request.headers.get('Authorization').split()[1])
                redis_store.delete(jti)

            return jsonify(user), 201
        return jsonify({"error": ERROR_UPDATE_USER}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    """Deletes an existing user record based on its ID."""
    return db.delete_user(id)



# Models API endpoints
@app.route("/models/<model_type>/<int:id>", methods=["GET"])
@jwt_required()
def get_model(model_type, id):
    """Retrieves a specific model data by its ID."""
    model = db.get_model(model_type, id)
    if model:
        return jsonify(model)
    return jsonify({"error": MODEL_NOT_FOUND}), 404


@app.route("/models", methods=["GET"])
@jwt_required()
def get_models():
    """Retrieves a specific model data by its ID."""

    models_ids = request.json.get('modelsIds')
    result = dict()
    for model_type, model_ids in models_ids.items():
        result[model_type] = db.get_models(model_type, model_ids)
    return jsonify(result)
    

@app.route("/search", methods=["GET"])
@jwt_required()
def search():
    """Retrieves a specific model data by its ID."""
    search_text = request.args.get('search_text')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    result = db.search(limit, offset, search_text)
    return jsonify(result)


@app.route("/models/<model_type>", methods=["POST"])
@jwt_required()
def create_model(model_type):
    """Creates a new model record based on the provided data."""
    model_data = request.json
    
    if not model_data:
        return jsonify({"error": MISSING_DATA}), 400
    
    try:
        model = db.save_model(model_data, model_type)
        if model:
            return jsonify(model), 201
        return jsonify({"error": ERROR_SAVE_MODEL}), 500
    except Exception as e:
        return jsonify({'error': str(e)})
        

@app.route("/models/<model_type>/<int:id>", methods=["PUT"])
@jwt_required()
def update_model(model_type, id):
    """Updates an existing model record based on the provided data."""
    model_data = request.json
    if not model_data:
        return jsonify({"error": MISSING_DATA}), 400
    
    try:
        model = db.update_model(id, model_type, model_data)
        if model:
            return jsonify(model), 201
        return jsonify({"error": ERROR_UPDATE_MODEL}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route("/models/<model_type>/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_model(model_type, id):
    """Deletes an existing model record based on its ID."""
    return db.delete_model(model_type, id)


@app.route('/backup', methods=['GET'])
@jwt_required()
def backup():
    password = request.json.get('password')
    db.create_new_backup(password)

    return send_file('backup.db', as_attachment=True)


# Run the Flask app
def run():
  db.initialize()
#   serve(app, host='0.0.0.0', port=5000)
  app.run(host='0.0.0.0', port=5000, debug=True)



if __name__ == "__main__":
    run()