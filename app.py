import os
from datetime import timedelta

from flask import Flask, request, jsonify, session, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL') or 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.secret_key = os.environ.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(weeks=2)


CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
ma = Marshmallow(app)
flask_bcrypy = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    country = db.Column(db.String(4), nullable=True)
    blogs = db.relationship('Blog', backref='user', lazy=True,
                            cascade='all, delete')
    schedules = db.relationship('Schedule', backref='user', lazy=True,
                                cascade='all, delete')


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(35), nullable=False)
    description = db.Column(db.String(35), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog
        include_fk = True


class ScheduleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Schedule
        include_fk = True


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'profile',
                  'avatar', 'blogs', 'schedules')
    blogs = fields.List(fields.Nested(
        lambda: BlogSchema(only=('title', 'content'))))
    schedules = fields.List(fields.Nested(
        lambda: ScheduleSchema(only=('title', 'description'))))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route('/api/v1/register', methods=['POST'])
def register():
    post_data = request.get_json()
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    db_user = User.query.filter_by(username=username, email=email).first()
    if db_user:
        return 'Username or Email All Ready Used', 409
    hashed_password = flask_bcrypy.generate_password_hash(
        password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    session.permanent = True
    session['username'] = username
    return jsonify({"message": "User Verified", "user_id": new_user.id, 'username': new_user.username})


@app.route('/api/v1/get_user/<username>')
def get_user(username):
    db_user = User.query.filter_by(username=username).first()
    if db_user is None:
        return "Username NOT found"
    return jsonify(user_schema.dump(db_user))


@app.route('/api/v1/get_all_users')
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/api/v1/edit_user/<user_id>', methods=['PATCH'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.username = request.json.get('username')
    user.email = request.json.get('email')
    user.state = request.json.get('state')
    user.country = request.json.get('country')
    db.session.commit()
    return jsonify(user_schema.dump(user))


@app.route('/api/v1/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return jsonify('User Deleted')
    return 'User Not Found', 404


@app.route('/api/v1/profile', methods=['PATCH'])
def add_profile():
    post_data = request.get_json()
    avatar = post_data.get('avatar')
    state = post_data.get('state')
    country = post_data.get('country')
    user_id = post_data.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    user.state = state
    user.country = country
    user.avatar = avatar
    db.session.commit()
    return jsonify(user_schema.dump())


@app.route('/api/v1/blog', methods=['POST'])
def add_blog():
    post_data = request.get_json()
    title = post_data.get('title')
    content = post_data.get('content')
    user_id = post_data.get('user_id')
    new_blog = Blog(title=title, content=content, user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(blog_schema.dump(new_blog))


@app.route('/api/v1/get_blog/<blog_id>')
def get_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    return jsonify(blog_schema.dump(blog))


@app.route('/api/v1/get_all_blogs', methods=['GET'])
def get_all_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


@app.route('/api/v1/edit_blog/<blog_id>', methods=['PATCH'])
def edit_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    blog.title = request.json.get('title')
    blog.content = request.json.get('content')
    db.session.commit()
    return jsonify(blog_schema.dump(blog))


@app.route('/api/v1/delete_blog/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return "Blog Deleted!"


@app.route('/api/v1/schedule', methods=['POST'])
def add_schedule():
    post_data = request.get_json()
    title = post_data.get('title')
    description = post_data.get('description')
    user_id = post_data.get('user_id')
    new_schedule = Schedule(
        title=title, description=description, user_id=user_id)
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify(schedule_schema.dump(new_schedule))


@app.route('/api/v1/get_schedule/<schedule_id>')
def get_schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    return jsonify(schedule_schema.dump(schedule))


@app.route('/api/v1/get_all_schedules', methods=['GET'])
def get_all_schedules():
    all_schedules = Schedule.query.all()
    result = schedules_schema.dump(all_schedules)
    return jsonify(result)


@app.route('/api/v1/edit_schedule/<schedule_id>', methods=['PATCH'])
def edit_schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    schedule.title = request.json.get('title')
    schedule.description = request.json.get('description')
    db.session.commit()
    return jsonify(schedule_schema.dump(schedule))


@app.route('/api/v1/delete_schedule/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return "Event Deleted!"


@app.route('/api/v1/login', methods=['POST'])
def login():
    post_data = request.get_json()
    db_user = User.query.filter_by(username=post_data.get('username')).first()
    if db_user is None:
        return "Username or Password Invalid", 404
    password = post_data.get('password')
    db_user_hashed_password = db_user.password
    valid_password = flask_bcrypy.check_password_hash(
        db_user_hashed_password, password)
    if valid_password:
        session.permanent = True
        session['username'] = post_data.get('username')
        return jsonify({"message": "User Verified", "user_id": db_user.id, 'username': db_user.username})
    return "Username or Password invalid"


@app.route('/api/v1/logged_in', methods=['GET'])
def logged_in():
    if 'username' in session:
        db_user = User.query.filter_by(username=session['username']).first()
        if db_user:
            return jsonify({"message": "User Loggedin Via Cookie", "user_id": db_user.id, 'username': db_user.username})
        else:
            return jsonify('Session Exists, but no user')
    else:
        return jsonify('Nope!')


@app.route('/api/v1/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify('Logged Out')


if __name__ == '__main__':
    app.run(debug=True)
