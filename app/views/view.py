from flask import jsonify, request

from flask.views import MethodView

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app import app, db

from app.models.models import User, Post, Coment, Topic

from app.schemas.schema import (
    PrivateUserSchema,
    PublicUserSchema,
    PostSchema,
    ComentSchema,
    TopicSchema,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from datetime import timedelta


class IndexMethod(MethodView):
    def get(self):
        return jsonify(Index="Ferrari")


app.add_url_rule("/", view_func=IndexMethod.as_view("Index"))


class UserMethod(MethodView):
    @jwt_required()
    def get(self, user_id=None):
        # Busco todos los usuarios
        if user_id is None:
            users = User.query.all()
            users_schema = PublicUserSchema().dump(users, many=True)
            return jsonify(users_schema)

        # Busco un unico usuario por su ID
        user = User.query.get(user_id)
        identity = get_jwt_identity()

        # Verifico que sea el usuario logeado
        if user.username == identity:
            user_schema = PrivateUserSchema().dump(user)
            return jsonify(user_schema)

        return jsonify(Error="Nope")

    def post(self):
        # Creo un nuevo usuario
        data = request.get_json()
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        password_hash = generate_password_hash(
            password=password, method="pbkdf2", salt_length=16
        )

        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Mensaje=f"Se creo el usuario: {username}")

    @jwt_required()
    def put(self, user_id):
        # Actualizar informacion de usuario segun id
        user = User.query.get(user_id)
        data = request.get_json()
        new_password = data.get("password")

        password_hash = generate_password_hash(
            password=new_password, method="pbkdf2", salt_length=16
        )

        user.password = password_hash
        db.session.commit()

        user_schema = PrivateUserSchema().dump(user)
        return jsonify(user_schema)

    @jwt_required()
    def delete(self, user_id):
        # Elimino un usuario segun id
        user = User.query.get(user_id)
        identity = get_jwt_identity()

        # Verifico que sea el usuario logeado
        if user.username == identity:
            db.session.delete(user)
            db.session.commit()
            return jsonify(Mensaje=f"User {user_id} deleted")

        return jsonify(Error="No hay permisos")


app.add_url_rule("/user", view_func=UserMethod.as_view("User"))
app.add_url_rule("/user/<user_id>", view_func=UserMethod.as_view("User_by_id"))


class LoginMethod(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(
            pwhash=user.password, password=password
        ):
            access_token = create_access_token(
                identity=user.username,
                expires_delta=timedelta(minutes=5),
                additional_claims={"id_user": user.id},
            )
            return jsonify({"Login": "Ok", "Token": access_token})
        return jsonify(Error="User or password wrong")


app.add_url_rule("/login", view_func=LoginMethod.as_view("Login"))


class PostMethod(MethodView):
    def get(self, post_id=None):
        # Todos los posts
        if post_id is None:
            posts = Post.query.all()
            post_schema = PostSchema().dump(posts, many=True)
            return jsonify(post_schema)

        # Post + sus respectivos comentarios
        post = Post.query.filter_by(id=post_id)
        post_schema = PostSchema().dump(post, many=True)
        coment = Coment.query.filter_by(post=post_id)
        coment_schema = ComentSchema().dump(coment, many=True)
        return jsonify(post_schema, coment_schema)

    @jwt_required()
    def post(self):
        # Creacion de un post
        data = request.get_json()

        jwt_data = get_jwt()

        title = data.get("title")
        topic = data.get("topic_id")
        content = data.get("content")
        user = jwt_data["id_user"]

        new_post = Post(
            title=title,
            topic=topic,
            content=content,
            user=user,
        )

        db.session.add(new_post)
        db.session.commit()
        return jsonify(Mensaje="New post added")


app.add_url_rule("/post", view_func=PostMethod.as_view("Post"))
app.add_url_rule("/post/<post_id>", view_func=PostMethod.as_view("Post_and_comments"))


class ComentMethod(MethodView):
    @jwt_required()
    def post(self):
        # Creacion de un comentario
        data = request.get_json()

        jwt_data = get_jwt()

        content = data.get("content")
        post_id = data.get("post_id")
        user = jwt_data["id_user"]

        new_post = Coment(
            content=content,
            user=user,
            post=post_id,
        )

        db.session.add(new_post)
        db.session.commit()
        return jsonify(Mensaje="New coment added")


app.add_url_rule("/coment", view_func=ComentMethod.as_view("Coment"))


class TopicMethod(MethodView):
    def get(self):
        topics = Topic.query.all()
        topic_schema = TopicSchema().dump(topics, many=True)
        return jsonify(topic_schema)

    @jwt_required()
    def post(self):
        data = request.get_json()

        name = data.get("name")

        new_topic = Topic(name=name)

        db.session.add(new_topic)
        db.session.commit()
        return jsonify(Mensaje="New topic added")


app.add_url_rule("/topic", view_func=TopicMethod.as_view("Topic"))