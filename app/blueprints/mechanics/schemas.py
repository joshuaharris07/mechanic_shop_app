from marshmallow import fields
from sqlalchemy import func
from app.models import Mechanic, db
from app.extensions import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
    
    ticket_count = fields.Method("get_ticket_count")

    def get_ticket_count(self, mechanic):
        count = db.session.query(func.count()).select_from(Mechanic).join(Mechanic.tickets).filter(Mechanic.id == mechanic.id).scalar()
        return count or 0

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)