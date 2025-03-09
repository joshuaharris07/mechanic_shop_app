from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema, return_service_ticket_schema, edit_service_ticket_schema
from marshmallow import ValidationError
from app.models import Inventory, ServiceTicket, Mechanic, db
from sqlalchemy import select
from app.utils.util import token_required


@service_tickets_bp.route('/', methods = ['GET'])
def get_service_tickets():
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(ServiceTicket)
        service_tickets = db.paginate(query, page=page, per_page=per_page)
        return service_tickets_schema.jsonify(service_tickets)
    except:
        query = select(ServiceTicket)
        service_tickets = db.session.execute(query).scalars().all()
        return service_tickets_schema.jsonify(service_tickets), 200

@service_tickets_bp.route('/my-tickets', methods = ['GET'])
@token_required
def get_tickets_by_customer(service_ticket_id):
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(ServiceTicket).where(ServiceTicket.customer_id == service_ticket_id)
        service_tickets = db.paginate(query, page=page, per_page=per_page)
        return service_tickets_schema.jsonify(service_tickets)
    except:
        query = select(ServiceTicket).where(ServiceTicket.customer_id == service_ticket_id)
        service_tickets = db.session.execute(query).scalars().all()
        return service_tickets_schema.jsonify(service_tickets), 200


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_service_ticket = ServiceTicket(
        vin=service_ticket_data["vin"],
        service_date=service_ticket_data["service_date"],
        service_desc=service_ticket_data["service_desc"],
        customer_id=service_ticket_data["customer_id"],
        )
    
    if "mechanic_ids" in request.json:

        for mechanic_id in service_ticket_data["mechanic_ids"]:
            query = select(Mechanic).where(Mechanic.id==mechanic_id)
            mechanic = db.session.execute(query).scalar()
            if mechanic:
                new_service_ticket.mechanics.append(mechanic)
            else:
                return jsonify({"message": "Invalid mechanic ID"}), 400
        
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return return_service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket was successfully deleted: {service_ticket_id}"}), 200


@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    try: 
        query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
        service_ticket = db.session.execute(query).scalars().first()
        if not service_ticket:
            return jsonify({"message": "Service ticket not found"}), 404
        
        request_data = request.json
        service_ticket_edits = edit_service_ticket_schema.load(request_data)

        if 'add_mechanic_ids' in service_ticket_edits and service_ticket_edits['add_mechanic_ids']:
            for mechanic_id in service_ticket_edits['add_mechanic_ids']:
                query = select(Mechanic).where(Mechanic.id == mechanic_id)
                mechanic = db.session.execute(query).scalars().first()

                if mechanic and mechanic not in service_ticket.mechanics:
                    service_ticket.mechanics.append(mechanic)

        if 'remove_mechanic_ids' in service_ticket_edits and service_ticket_edits['remove_mechanic_ids']:
            for mechanic_id in service_ticket_edits['remove_mechanic_ids']:
                query = select(Mechanic).where(Mechanic.id == mechanic_id)
                mechanic = db.session.execute(query).scalars().first()

                if mechanic and mechanic in service_ticket.mechanics:
                    service_ticket.mechanics.remove(mechanic)
        
        if 'add_part_id' in service_ticket_edits and service_ticket_edits['add_part_id']:
            query = select(Inventory).where(Inventory.id == service_ticket_edits['add_part_id'])
            part = db.session.execute(query).scalars().first()

            if part and part not in service_ticket.parts:
                service_ticket.parts.append(part)
        
        if not any(key in request_data for key in ['add_mechanic_ids', 'remove_mechanic_ids', 'add_part_id']):
            return jsonify({"message": "Invalid request, no changes to update"}), 400

        db.session.commit()
        return return_service_ticket_schema.jsonify(service_ticket)

    except ValidationError as err:
            return jsonify(err.messages), 400