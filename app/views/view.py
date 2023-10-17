from flask import (
    jsonify,
    request,
    render_template,
)

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
)

from app.schemas.schema import(
    UserSchema,
    PostSchema,
)

from werkzeug.security import(
    generate_password_hash,
    check_password_hash,
)

from datetime import timedelta

@app.route('/')
def index():
    return jsonify(mensaje='Mattia Binotto')

@app.route('/user', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
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
    
    if request.method == 'GET':
        users = User.query.all()
        users_schema = UserSchema().dump(users, many=True)
        return jsonify(users_schema)

@app.route('/user/<id_user>', methods=['PUT', 'DELETE', 'GET'])
def users_by_id(id_user):
    if request.method == 'GET':
        # Busco un unico usuario por su ID
        user = User.query.get(id_user)
        # Lo convierto en un esquema
        user_schema = UserSchema().dump(user)
        return jsonify(user_schema)

    if request.method == 'DELETE':
        # Busco un unico usuario por su ID
        user = User.query.get(id_user)
        # Elimino el usuario
        db.session.delete(user)
        db.session.commit()
        return jsonify(Mensaje=f"User {id_user} deleted")
    
    if request.method == 'PUT':
        # Busco un unico usuario por su ID a modificar
        user = User.query.get(id_user)
        # Info a modificar
        data = request.get_json()
        new_password = data.get('password')

        password_hash = generate_password_hash(password=new_password, method="pbkdf2", salt_length=16)

        user.password = password_hash
        db.session.commit()

        user_schema = UserSchema().dump(user)
        return jsonify(user_schema)
    
@app.route('/login', methods=['POST'])
def login():
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

@app.route('/post', methods=['POST', 'GET'])
def posts():
    if request.method == 'POST':
        data = request.get_json()

        title = data.get('title')
        content = data.get('content')
        user = data.get('user_id')

        new_post = Post(
            title=title,
            content=content,
            user=user,
        )
        
        db.session.add(new_post)
        db.session.commit()
        return jsonify(Mensaje='Se agrego nuevo post')
    
    if request.method == 'GET':
        posts = Post.query.all()
        post_schema = PostSchema().dump(posts, many=True)
        return jsonify(post_schema)
