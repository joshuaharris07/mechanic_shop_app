from flask import request, jsonify
from app.blueprints.customers import   customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select
from app.extensions import cache
from app.utils.util import encode_token, token_required


@customers_bp.route('/login', methods = ['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "successfully logged in",
            "token": token
        }

        return jsonify(response), 200
    else: 
        return jsonify({"message": "invalid email or password"})

@customers_bp.route('/', methods = ['GET'])
@cache.cached(timeout=10) #Added cache to customers so that the information is more readily accessible to the shop as it wouldn't be updated very regularly.
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

    new_customer = Customer(name=customer_data['name'], phone=customer_data['phone'], email=customer_data['email'], password=customer_data['password'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer added successfully"}), 201

@customers_bp.route('/', methods = ['PUT'])
@token_required
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

@customers_bp.route('/', methods = ['DELETE'])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200


@customers_bp.route("/search", methods=['GET']) #TODO make sure this works as intended with finding customers
def search_customer():
    name = request.args.get("name")

    query = select(Customer).where(Customer.name.like(f'%{name}%'))
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers)