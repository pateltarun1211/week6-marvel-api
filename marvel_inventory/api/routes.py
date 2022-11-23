from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Superhero, superhero_schema, superheroes_schema
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

@api.route('/superheroes', methods = ['POST'])
@token_required
def create_superhero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = datetime.utcnow()
    user_token = current_user_token.token
    
    print(f"User Token: {current_user_token.token}")
    
    superhero = Superhero(name, description, comics_appeared_in, super_power, date_created, user_token=user_token)
    
    db.session.add(superhero)
    db.session.commit()
    
    response = superhero_schema.dump(superhero)
    
    return jsonify(response)

@api.route('/superheroes', methods = ['GET'])
@token_required
def get_superheroes(current_user_token):
    owner = current_user_token.token
    superheroes = Superhero.query.filter_by(user_token=owner).all()
    response = superheroes_schema.dump(superheroes)
    return jsonify(response)

@api.route('/superheroes/<id>', methods = ['GET'])
@token_required
def get_superhero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        superhero = Superhero.query.get(id)
        response = superhero_schema.dump(superhero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

@api.route('superheroes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_superhero(current_user_token, id):
    superhero = Superhero.query.get(id)
    superhero.name = request.json['name']
    superhero.description = request.json['description']
    superhero.comics_appeared_in = request.json['comics_appeared_in']
    superhero.super_power = request.json['super_power']
    superhero.date_created = datetime.utcnow()
    user_token = current_user_token.token
    
    db.session.commit()
    response = superhero_schema.dump(superhero)
    return jsonify(response)

@api.route('/superheroes/<id>', methods = ['DELETE'])
@token_required
def delete_superhero(current_user_token, id):
    superhero = Superhero.query.get(id)
    db.session.delete(superhero)
    db.session.commit()
    response = superhero_schema.dump(superhero)
    return jsonify(response)