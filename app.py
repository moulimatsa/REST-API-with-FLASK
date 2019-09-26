from flask import Flask, request, jsonify, redirect, url_for, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from flask_wtf import Form, validators
from wtforms.validators import DataRequired, Email, Length
from wtforms_validators import ActiveUrl, Alpha, DisposableEmail
import os
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

import psycopg2

from datetime import datetime

app = Flask(__name__)

CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Here i have used PostgreSQL database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pg1234@localhost/home_credit_dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db

db = SQLAlchemy(app)

# Init ma

ma = Marshmallow(app)


class biodata(db.Model):
    __tablename__ = 'register'

    email = db.Column(db.String(100), primary_key=True, unique=True)
    name = db.Column(db.String(100))
    profileId = db.Column(db.Integer, primary_key=False, unique=True, autoincrement=True)
    employed = db.Column(db.String(100))
    familyMembersCount = db.Column(db.Integer)
    familyStatus = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    incomeType = db.Column(db.String(100))
    mobile = db.Column(db.String(100),unique=True)
    occupationType = db.Column(db.String(100))
    ownCar = db.Column(db.String(100))
    ownCarAge = db.Column(db.Integer)
    address = db.Column(db.String(100))
    child = db.Column(db.Integer)
    dob = db.Column(db.String(100))
    educationType = db.Column(db.String(100))

    @classmethod
    def is_email_taken(cls, email):
        return db.session.query(db.exists().where(biodata.email == email)).scalar()

    @classmethod
    def is_mobile_taken(cls, mobile):
        return db.session.query(db.exists().where(biodata.mobile == mobile)).scalar()

    def __init__(self, name, email, employed, familyMembersCount, familyStatus, gender, incomeType, mobile,
                 occupationType, ownCar, ownCarAge, address,
                 child, dob, educationType):
        self.name = name
        self.email = email
        self.employed = employed
        self.familyMembersCount = familyMembersCount
        self.familyStatus = familyStatus
        self.gender = gender
        self.incomeType = incomeType
        self.mobile = mobile
        self.occupationType = occupationType
        self.ownCar = ownCar
        self.ownCarAge = ownCarAge
        self.address = address
        self.child = child
        self.dob = dob
        self.educationType = educationType

    def __repr__(self):
        return '<email {}>'.format(self.email)

    def serialize(self):
        return {

            'profileId': self.profileId,
            'name': self.name,
            'email': self.email,
            'employed': self.employed,
            'familyMembersCount': self.familyMembersCount,
            'familyStatus': self.familyStatus,
            'gender': self.gender,
            'incomeTYPE': self.incomeType,
            'mobile': self.mobile,
            'occupationType': self.occupationType,
            'ownCar': self.ownCar,
            'ownCarAge': self.ownCarAge,
            'address': self.address,
            'child': self.child,
            'dob': self.dob,
            'educationType': self.educationType

        }


# details Schema

class biodataSchema(ma.Schema):
    class Meta:
        fields = (
            'profileId', 'name', 'email', 'employed', 'familyMembersCount', 'familyStatus', 'gender', 'incomeType',
            'mobile',
            'occupationType', 'ownCar', 'ownCarAge', 'address',
            'child', 'dob', 'educationType')


biodata_schema = biodataSchema(strict=True)

biodated_schema = biodataSchema(many=True, strict=True)


'''def validate_email(email):

    user = biodata.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('That email is taken. Please choose another.')
    else:
        pass'''


@app.route('/')
@cross_origin()
def index():
    return "hello!world"


# Create a detail



@app.route('/biodata/add', methods=['POST'])
@cross_origin()
def add_details():
    name = request.json['name']

    employed = request.json['employed']
    familyMembersCount = request.json['familyMembersCount']
    familyStatus = request.json['familyStatus']
    gender = request.json['gender']
    incomeType = request.json['incomeType']
    occupationType = request.json['occupationType']
    ownCar = request.json['ownCar']
    ownCarAge = request.json['ownCarAge']
    address = request.json['address']
    child = request.json['child']
    dob = request.json['dob']
    educationType = request.json['educationType']

    if biodata.is_email_taken(request.json['email']):
        return jsonify({'email': 'This email is already taken!'}), 409
    else:
        email = request.json['email']


    if biodata.is_mobile_taken(request.json['mobile']):
        return jsonify({'mobile':'This mobile no. is already taken'}),409
    else:
        mobile = request.json['mobile']

    new_biodata = biodata(name, email, employed, familyMembersCount, familyStatus, gender, incomeType, mobile,
                          occupationType, ownCar, ownCarAge, address,
                          child, dob, educationType)

    db.session.add(new_biodata)

    db.session.commit()

    return biodata_schema.jsonify(new_biodata)


'''    if 'username' not in request.json:
        return jsonify({'username': 'must include username'})
    if 'email' not in request.json:
        return jsonify({'email': 'must include email'})
    if 'password' not in request.json:
        return jsonify({'password' : 'must include password' })

    if User.is_user_name_taken(request.json['username']):
         return jsonify({'username': 'This username is already taken!'}), 409
    if User.is_user_name_taken(request.json['username']):
        return jsonify({'username': 'This username is already taken!'}), 409
    if request.json :
        hashed_password = generate_password_hash(request.json['password'], method='sha256')
        new_user = User(username=request.json['username'], email=request.json['email'], password=hashed_password)
        
        return jsonify({'user': 'user created successfully'}), 201
    return jsonify({'username': 'must include username',
            'password': 'must include password',
            'email' : 'must include email' })'''

# Get All details

@app.route('/biodata/get_all', methods=['GET'])
@cross_origin()
def get_details():
    all_biodata = biodata.query.all()

    result = biodated_schema.dump(all_biodata)

    return jsonify(result.data)


# Get Single detail

@app.route('/biodata/get/<email>', methods=['GET'])
@cross_origin()
def get_product(email):
    detailsew = biodata.query.get(email)

    return biodata_schema.jsonify(detailsew)


# update a detail

@app.route('/biodata/update/<email>', methods=['PUT'])
@cross_origin()
def update_details(email):
    detailk = biodata.query.get(email)

    name = request.json['name']
    email = request.json['email']
    employed = request.json['employed']
    familyMembersCount = request.json['familyMembersCount']
    familyStatus = request.json['familyStatus']
    gender = request.json['gender']
    incomeType = request.json['incomeType']
    mobile = request.json['mobile']
    occupationType = request.json['occupationType']
    ownCar = request.json['ownCar']
    ownCarAge = request.json['ownCarAge']
    address = request.json['address']
    child = request.json['child']
    dob = request.json['dob']
    educationType = request.json['educationType']

    biodata.name = name
    biodata.email = email
    biodata.employed = employed
    biodata.familyMembersCount = familyMembersCount
    biodata.familyStatus = familyStatus
    biodata.gender = gender
    biodata.incomeType = incomeType
    biodata.mobile = mobile
    biodata.occupationType = occupationType
    biodata.ownCar = ownCar
    biodata.ownCarAge = ownCarAge
    biodata.address = address
    biodata.child = child
    biodata.dob = dob
    biodata.educationType = educationType

    db.session.commit()

    return biodata_schema.jsonify(detailk)


# delete a detail
@app.route('/biodata/delete/<email>', methods=['DELETE'])
@cross_origin()
def delete_product(email):
    detaileds = biodata.query.get(email)

    db.session.delete(detaileds)

    db.session.commit()

    return biodata_schema.jsonify(detaileds)


# Run Server

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
