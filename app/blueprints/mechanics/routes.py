from flask import request, jsonify
from app.blueprints.mechanics import   mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select
from app.extensions import cache

@mechanics_bp.route('/', methods = ['GET'])
# @cache.cached(timeout=10) #Added cache to mechanics so that the information is more readily accessible to the shop as it wouldn't need to be updated very regularly.
def get_mechanics():
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page)
        return mechanics_schema.jsonify(mechanics)
    except:
        query = select(Mechanic)
        result = db.session.execute(query).scalars().all()
        return mechanics_schema.jsonify(result), 200

@mechanics_bp.route('/', methods = ['POST'])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_mechanic = Mechanic(name=mechanic_data['name'], phone=mechanic_data['phone'], email=mechanic_data['email'], salary=mechanic_data['salary'])
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/<int:mechanic_id>', methods = ['PUT'])
def update_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic == None:
        return jsonify({"message": "Invalid mechanic ID"})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:mechanic_id>', methods = ['DELETE'])
def delete_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic == None:
        return jsonify({"message": "Invalid mechanic ID"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic removed successfully"}), 200


@mechanics_bp.route("/most-tickets", methods=['GET'])
def sort_mechanics_by_tickets():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    print(mechanics)
    mechanics.sort(key = lambda mechanic: len(mechanic.tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics)