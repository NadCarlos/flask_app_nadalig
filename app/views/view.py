from flask import (
    jsonify,
    request,
    render_template,
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


@app.route('/')
def index():
    return jsonify(mensaje='index.html')

@app.route('/user', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        new_user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Mensaje=f"Se creo el usuario: {username}")
    
    if request.method == 'GET':
        users = User.query.all()
        users_schema = UserSchema().dump(users, many=True)
        return jsonify(users_schema)

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
        post = User.query.all()
        post_schema = PostSchema().dump(users, many=True)
        return jsonify(post_schema)
