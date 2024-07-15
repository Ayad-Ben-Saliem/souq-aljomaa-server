from flask import Flask, request, jsonify, send_file
from db import Database
from constants import *
from waitress import serve

def create_app():
    return Flask(__name__);

# Initialize Flask app
app = create_app()

db = Database()

# API endpoints
@app.route("/models/<model_type>/<int:id>", methods=["GET"])
def get_model(model_type, id):
    """Retrieves a specific model data by its ID."""
    model = db.get_model(model_type, id)
    if model:
        return jsonify(model)
    return jsonify({"error": MODEL_NOT_FOUND}), 404

@app.route("/models", methods=["GET"])
def get_models():
    """Retrieves a specific model data by its ID."""
    json = request.get_json()
    models_ids = json['modelsIds']
    result = dict()
    for model_type, model_ids in models_ids.items():
        result[model_type] = db.get_models(model_type, model_ids)
    if result:
        return jsonify(result)
    return jsonify({"error": MODEL_NOT_FOUND}), 404


@app.route("/search", methods=["GET"])
def search():
    """Retrieves a specific model data by its ID."""
    search_text = request.args.get('search_text')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    result = db.search(limit, offset, search_text)
    return jsonify(result)


@app.route("/models/<model_type>", methods=["POST"])
def create_model(model_type):
    """Creates a new model record based on the provided data."""
    model_data = request.get_json()
    if not model_data:
        return jsonify({"error": MISSING_DATA}), 400
    model = db.save_model(model_data, model_type)
    if model:
        return jsonify(model), 201
    return jsonify({"error": SAVE_ERROR}), 500


@app.route("/models/<model_type>/<int:id>", methods=["PUT"])
def update_model(model_type, id):
    """Updates an existing model record based on the provided data."""
    model_data = request.get_json()
    if not model_data:
        return jsonify({"error": MISSING_DATA}), 400
    model = db.update_model(model_data, model_type, id)
    if model:
        return jsonify(model)
    return jsonify({"error": UPDATE_ERROR}), 500

@app.route("/models/<model_type>/<int:id>", methods=["DELETE"])
def delete_model(model_type, id):
    """Deletes an existing model record based on its ID."""
    return db.delete_model(model_type, id)


@app.route('/backup', methods=['GET'])
def update():
    db.create_new_backup()

    return send_file('backup.db', as_attachment=True)


# Run the Flask app
def run():
  db.initialize()
  serve(app, host='0.0.0.0', port=5000)
#   app.run(host='0.0.0.0', port=5000)
#   app.run(debug=True)



if __name__ == "__main__":
    run()