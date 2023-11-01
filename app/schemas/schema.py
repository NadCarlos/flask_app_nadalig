from app import ma
from marshmallow import fields


class PublicUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()


class PrivateUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()


class TopicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    user = fields.Integer()
    user_obj = fields.Nested(PrivateUserSchema, exclude=['id', 'password'])
    topic = fields.Integer()
    topic_obj = fields.Nested(TopicSchema, exclude=['id'])


class ComentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String()
    post = fields.Integer()
    user = fields.Integer()
    user_obj = fields.Nested(PrivateUserSchema, exclude=['id', 'password'])