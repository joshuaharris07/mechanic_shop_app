from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)
    customer = fields.Nested("CustomerSchema")
    class Meta:
        model = ServiceTicket
        fields = ("mechanic_ids", "vin", "service_date", "service_desc", "customer_id", "mechanics", "customer")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])