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
    drink = Drink(name=request.json['name'],description=request.json['description'])

    db.session.add(drink)
    db.session.commit()

    return {'id': drink.id}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)

    if drink is None:
        return {"error": "Drink not found"}, 404

    db.session.delete(drink)
    db.session.commit()

    return {"message": "Drink deleted"}