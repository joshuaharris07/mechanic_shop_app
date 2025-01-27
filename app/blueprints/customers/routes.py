from flask import request, jsonify
from app.blueprints.customers import   customers_bp
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select, delete

@customers_bp.route('/', methods = ['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(result), 200

@customers_bp.route('/', methods = ['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_customer = Customer(name=customer_data['name'], phone=customer_data['phone'], email=customer_data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer added successfully"}), 201

@customers_bp.route('/<int:customer_id>', methods = ['PUT'])
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for field, value in customer_data.items():
        setattr(customer, field, value)
    
    db.session.commit()
    return jsonify({"message": "Customer details updated successfully"}), 200

@customers_bp.route('/<int:customer_id>', methods = ['DELETE'])
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200