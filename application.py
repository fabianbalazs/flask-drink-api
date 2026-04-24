from flask import Flask, request, send_file
from models import db, Drink
import config
import csv
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

EXPORT_DIR = 'exports'
os.makedirs(EXPORT_DIR, exist_ok=True)


@app.route('/')
def index():
    return "Hello!"


@app.route('/drinks')
def get_drinks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        pagination = Drink.query.paginate(page=page, per_page=per_page, error_out=False)

        output = [
            {'id': d.id, 'name': d.name, 'description': d.description}
            for d in pagination.items
        ]

        return {
            "drinks": output,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }

    except Exception as e:
        return {"error": "Failed to retrieve drinks", "details": str(e)}, 500



@app.route('/drinks/<int:id>')
def get_drink(id):
    try:
        drink = Drink.query.get_or_404(id)
        return {
            "id": drink.id,
            "name": drink.name,
            "description": drink.description
        }

    except Exception as e:
        return {"error": "Failed to retrieve drink", "details": str(e)}, 500




@app.route('/drinks', methods=['POST'])
def add_drink():
    try:
        data = request.get_json()

        if data is None:
            return {"error": "Request must be JSON"}, 400

        errors = []

        if 'name' not in data:
            errors.append("Name is required")
        if 'description' not in data:
            errors.append("Description is required")

        if errors:
            return {"errors": errors}, 400

        name = data['name'].strip()
        description = data['description'].strip()

        if not name:
            errors.append("Name cannot be empty")
        if not description:
            errors.append("Description cannot be empty")
        if len(description) > 150:
            errors.append("Description must be less than 150 characters")

        if errors:
            return {"errors": errors}, 400

        existing_drink = Drink.query.filter_by(name=name).first()
        if existing_drink:
            return {"error": "Drink already exists"}, 400

        drink = Drink(name=name, description=description)
        db.session.add(drink)
        db.session.commit()

        return {
            "id": drink.id,
            "name": drink.name,
            "description": drink.description
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to add drink", "details": str(e)}, 500




@app.route('/drinks/<int:id>', methods=['PUT'])
def put_drink(id):
    try:
        data = request.get_json()
        drink = Drink.query.get(id)

        if drink is None:
            return {"error": "Drink not found"}, 404
        if not data:
            return {"error": "Invalid JSON"}, 400
        if 'name' not in data or 'description' not in data:
            return {"error": "Missing fields"}, 400

        name = data['name'].strip()
        description = data['description'].strip()

        if not name or not description:
            return {"error": "Fields cannot be empty"}, 400

        drink.name = name
        drink.description = description
        db.session.commit()

        return {
            "id": drink.id,
            "name": drink.name,
            "description": drink.description
        }

    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update drink", "details": str(e)}, 500




@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    try:
        drink = Drink.query.get(id)

        if drink is None:
            return {"error": "Drink not found"}, 404

        db.session.delete(drink)
        db.session.commit()

        return {"message": "Drink deleted"}

    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete drink", "details": str(e)}, 500



@app.route('/drinks/export/csv')
def export_drinks_csv():
    try:
        drinks = Drink.query.all() #request drinks
        filepath = os.path.join(EXPORT_DIR, 'drinks.csv') #path connection, giving name to file

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) #csv writer points to the recetnly opened file
            writer.writerow(['id', 'name', 'description']) #header
            for d in drinks:
                writer.writerow([d.id, d.name, d.description]) #writing all datas to the file

        return send_file(filepath, mimetype='text/csv', as_attachment=True,
                         download_name='drinks.csv') #giving the file back to user

    except Exception as e:
        return {"error": "CSV export failed", "details": str(e)}, 500



@app.route('/drinks/export/json')
def export_drinks_json():
    try:
        drinks = Drink.query.all() #request drinks
        output = [
            {'id': d.id, 'name': d.name, 'description': d.description}
            for d in drinks
        ]#giving all data back as list of dictionaries
        filepath = os.path.join(EXPORT_DIR, 'drinks.json') #path and name

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False) #writing out all dates formally (indent) and with non ascii characters

        return send_file(filepath, mimetype='application/json', as_attachment=True,
                         download_name='drinks.json') #giving back file to user

    except Exception as e:
        return {"error": "JSON export failed", "details": str(e)}, 500



@app.errorhandler(400)
def bad_request(e):
    return {"error": "Bad request", "details": str(e)}, 400

@app.errorhandler(404)
def not_found(e):
    return {"error": "Resource not found"}, 404

@app.errorhandler(405)
def method_not_allowed(e):
    return {"error": "Method not allowed"}, 405

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return {"error": "Internal server error"}, 500
