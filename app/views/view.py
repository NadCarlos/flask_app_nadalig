from flask import (
    jsonify,
    request
)

from flask.views import MethodView

from flask_jwt_extended import(
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app import app, db

from app.models.models import(
    User,
    Post,
    Coment,
)

from app.schemas.schema import(
    UserSchema,
    PostSchema,
    ComentSchema,
)

from werkzeug.security import(
    generate_password_hash,
    check_password_hash,
)

from datetime import timedelta

@app.route('/')
def index():
    return jsonify(mensaje='Ford')

class UserMethod(MethodView):

    def get(self, user_id = None):

        # Busco todos los usuarios
        if user_id is None:
            users = User.query.all()
            users_schema = UserSchema().dump(users, many=True)
            return jsonify(users_schema)
        
        # Busco un unico usuario por su ID
        user = User.query.get(user_id)
        user_schema = UserSchema().dump(user)
        return jsonify(user_schema)

    def post(self):

        #Creo un nuevo usuario
        data = request.get_json()
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        password_hash = generate_password_hash(password=password, method="pbkdf2", salt_length=16)

        new_user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Mensaje=f"Se creo el usuario: {username}")
    
    def put(self, user_id):

        # Actualizar informacion de usuario segun id
        user = User.query.get(user_id)
        data = request.get_json()
        new_password = data.get('password')

        password_hash = generate_password_hash(password=new_password, method="pbkdf2", salt_length=16)

        user.password = password_hash
        db.session.commit()

        user_schema = UserSchema().dump(user)
        return jsonify(user_schema)

    def delete(self, user_id):

        # Elimino un usuario segun id
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(Mensaje=f"User {user_id} deleted")

app.add_url_rule('/user',view_func=UserMethod.as_view('User'))
app.add_url_rule('/user/<user_id>',view_func=UserMethod.as_view('User_by_id'))


class LoginMethod(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(
            pwhash = user.password,
            password = password
        ):
            access_token = create_access_token(
                identity=user.username,
                expires_delta=timedelta(minutes=2),
                additional_claims={'id_user:':user.id}
            )
            return jsonify(
                {
                "Login":"Ok",
                "Token":access_token
                }
            )
        return jsonify(Error= "User or password wrong")
    
app.add_url_rule('/login',view_func=LoginMethod.as_view('Login'))


class PostMethod(MethodView):
    def get(self):
        posts = Post.query.all()
        post_schema = PostSchema().dump(posts, many=True)
        return jsonify(post_schema)

    def post(self):
        data = request.get_json()

        title = data.get('title')
        topic = data.get('topic_id')
        content = data.get('content')
        user = data.get('user_id')

        new_post = Post(
            title=title,
            topic=topic,
            content=content,
            user=user,
        )
        
        db.session.add(new_post)
        db.session.commit()
        return jsonify(Mensaje='Se agrego nuevo post')

app.add_url_rule('/post',view_func=PostMethod.as_view('Post'))

@app.route('/coment', methods=['POST', 'GET'])
def coment():
    coment = Coment.query.all()
    coment_schema = ComentSchema().dump(coment, many=True)
    return jsonify(coment_schema)