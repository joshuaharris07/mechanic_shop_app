from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)
    customer = fields.Nested("CustomerSchema")
    parts = fields.Nested("InventorySchema", many=True)
    class Meta:
        model = ServiceTicket
        fields = ("id", "mechanic_ids", "vin", "service_date", "service_desc", "customer_id", "mechanics", "customer", "parts")

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

class AddPartServiceTicketSchema(ma.Schema):
    add_part_id = fields.Int(required=True)
    class Meta:
        fields = ("add_part_id",)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_service_ticket_schema = EditServiceTicketSchema()
add_part_service_ticket_schema = AddPartServiceTicketSchema()