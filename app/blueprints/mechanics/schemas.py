from marshmallow import fields
from app.models import Mechanic
from app.extensions import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
    
    ticket_count = fields.Integer()

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)