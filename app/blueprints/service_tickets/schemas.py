from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema): #TODO when I get the service tickets it is sending me duplicate info.
    mechanics = fields.Nested("MechanicSchema", many=True)
    customer = fields.Nested("CustomerSchema")
    parts = fields.Nested("InventorySchema", many=True)
    class Meta:
        model = ServiceTicket
        fields = ("id", "mechanic_ids", "vin", "service_date", "service_desc", "customer_id", "mechanics", "customer", "parts")

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=False)
    remove_mechanic_ids = fields.List(fields.Int(), required=False)
    add_part_id = fields.Int(required=False)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids", "add_part_id")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_service_ticket_schema = EditServiceTicketSchema()