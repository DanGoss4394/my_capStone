import os
from datetime import timedelta

from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from flask_bcrypt import Bcrypt


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')


CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
ma = Marshmallow(app)
flask_bcrypy = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    profile = db.relationship('Profile', uselist=False, back_populates=False)
    blogs = db.relationship('Blog', backref='user', lazy=True)
    schedules = db.relationship('Schedule', backref='user', lazy=True)

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), nullable=True)
    country = db.Column(db.String(4), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates=False)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(35), nullable=False)
    description = db.Column(db.String(35), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True


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
        fields = ('id', 'username', 'email', 'profile', 'blogs', 'schedules')
    profile = fields.Nested(ProfileSchema)
    blogs = fields.List(fields.Nested(BlogSchema))
    schedules = fields.List(fields.Nested(ScheduleSchema))
#     profiles = fields.List(fields.Nested(ProfileSchema))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
profile_schema = ProfileSchema()


@app.route("/")
def hello_world():
    user = User.query.first()
    profile = Profile.query.first()
    print(user_schema.dump(user))
    print(profile_schema.dump(profile))
    print(user.profile)
    return render_template('home.html')


@app.route('/add-data/<max>')
def add_data(max):
    done = False
    for num in range(1, int(max)):
        user = User(
            username=f'test{num}', email=f'test{num}@test.com', password=f'test{num}')
        db.session.add(user)
        db.session.commit()
        profile = Profile(state=f"CO", country=f"USA", user_id=user.id)
        db.session.add(profile)
        db.session.commit()
    return 'Users added'


@app.route('/api/v1/register', methods=['POST'])
def register():
    post_data = request.get_json()
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    hashed_password = flask_bcrypy.generate_password_hash(
        password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(session)
    return jsonify(user_schema.dump(new_user))


@app.route('/api/v1/profile', methods=['POST'])
def add_profile():
    post_data = request.get_json()
    state = post_data.get('state')
    country = post_data.get('country')
    new_profile = Profile(state=state, country=country)
    db.session.add(new_profile)
    db.session.commit()
    return jsonify(profile_schema.dump(new_profile))


if __name__ == '__main__':
    app.run(debug=True)
