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
        return jsonify({"message": "Invalid email or password"}), 400


@customers_bp.route('/', methods = ['GET'])
# @cache.cached(timeout=10) #Added cache to customers so that the information is more readily accessible to the shop as it wouldn't be updated very regularly.
def get_customers():
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200

@customers_bp.route('/', methods = ['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_customer = Customer(name=customer_data['name'], phone=customer_data['phone'], email=customer_data['email'], password=customer_data['password'])
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

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
        if value not in [None, ""]:
            setattr(customer, field, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/', methods = ['DELETE'])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Successfully deleted customer {customer_id}"}), 200


@customers_bp.route("/search", methods=['GET'])
def search_customer():
    try: 
        name = request.args.get("name")
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer).where(Customer.name.like(f'%{name}%'))
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        name = request.args.get("name")
        query = select(Customer).where(Customer.name.like(f'%{name}%'))
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers)