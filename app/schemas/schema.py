from app import ma
from marshmallow import fields
from app.models.models import User
 
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()

class ComentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String()
    user = fields.Integer()
    user = fields.Integer()
    user_obj = fields.Nested(UserSchema)

class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    user = fields.Integer()
    user_obj = fields.Nested(UserSchema)
    coment = fields.Integer()
    coment_obj = fields.Nested(ComentSchema)