from flask import request, jsonify
from app.blueprints.inventory import inventory_bp
from .schemas import inventories_schema, inventory_schema
from marshmallow import ValidationError
from app.models import Inventory, db
from sqlalchemy import select
from app.extensions import cache


@inventory_bp.route('/', methods = ['GET'])
def get_inventory():
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Inventory)
        inventory = db.paginate(query, page=page, per_page=per_page)
        return inventory_schema.jsonify(inventory)
    except:
        query = select(Inventory)
        inventory = db.session.execute(query).scalars().all()
        return inventories_schema.jsonify(inventory), 200


@inventory_bp.route("/", methods=["POST"])
def create_part():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_part = Inventory(
        name=part_data["name"],
        price=part_data["price"]
        )
        
    db.session.add(new_part)
    db.session.commit()
    
    return inventory_schema.jsonify(new_part), 201


@inventory_bp.route("/<int:part_id>", methods=['DELETE'])
def delete_part(part_id):
    query = select(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query).scalars().first()

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part was successfully deleted: {part_id}"}), 200


@inventory_bp.route("/<int:part_id>", methods=['PUT'])
def update_part(part_id):
    query = select(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query).scalars().first()

    if part == None:
        return jsonify({"message": "Invalid part ID"})
    
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for field, value in part_data.items():
        setattr(part, field, value)
    
    db.session.commit()
    return inventory_schema.jsonify(part), 200