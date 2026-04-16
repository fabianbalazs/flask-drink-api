from flask import Flask, request
from models import db, Drink
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route('/')
def index():
    return "Hello!"

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []

    for drink in drinks:
        drink_data = {
            'name': drink.name,
            'description': drink.description
        }
        output.append(drink_data)

    return {"drinks": output}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)

    return {
        "name": drink.name,
        "description": drink.description
    }


@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.get_json()
    if data:
        name = data.get('name')

    if not data:
        return {"error": "Request must be JSON"}, 400

    errors = []

    existing_drink = Drink.query.filter_by(name=name).first()
    if existing_drink:
        return {"error": "Drink already exists"}, 400

    if 'name' not in data:
        errors.append("Name is required")
    if 'description' not in data:
        errors.append("Description is required")

    if errors:
        return {"errors": errors}, 400

    name = data['name'].strip()
    description = data['description'].strip()

    if not name:
        errors.append("name cannot be empty")

    if len(description) > 150:
        errors.append("description must be less than 150 characters")

    if not description:
        errors.append("description cannot be empty")

    if errors:
        return {"errors": errors}, 400

    drink = Drink(name=name, description=description)

    db.session.add(drink)
    db.session.commit()

    return {
        "id": drink.id,
        "name": drink.name,
        "description": drink.description
    }, 201


@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)

    if drink is None:
        return {"error": "Drink not found"}, 404

    db.session.delete(drink)
    db.session.commit()

    return {"message": "Drink deleted"}


@app.route('/drinks/<int:id>', methods=['PUT'])
def put_drink(id):
    data = request.get_json()
    drink = Drink.query.get(id)

    if not data:
        return {"error": "Invalid JSON"}, 400

    if 'name' not in data or 'description' not in data:
        return {"error": "Missing fields"}, 400

    name = data['name'].strip()
    description = data['description'].strip()

    if not name or not description:
        return {"error": "Empty fields"}, 400

    drink.name = name
    drink.description = description

    db.session.commit()

    return {
        'id': drink.id,
        "name": drink.name,
        "description" : drink.description}
