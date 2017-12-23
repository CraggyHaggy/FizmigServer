import datetime
import random
from functools import wraps

import jwt
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from models import Castle, Unit, User, db


# TODO: authorization logic
# (Implement SignOut, Tokens expiration, (Multiple errors)?).

@app.route("/sign_up", methods=['POST'])
def sign_up():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)

    if not username:
        return make_error(400, 'Username is required')
    if not password:
        return make_error(400, 'Password is required')
    if User.query.filter_by(username=username).first() is not None:
        return make_error(400, 'This username is already exists')
    if len(username) > User.max_username_length:
        return make_error(400, 'Username length must be less than ' + str(
            User.max_username_length) + ' characters')

    user = User(username,
                generate_password_hash(password, method='pbkdf2:sha512'))
    db.session.add(user)
    db.session.commit()

    return jsonify(201)


@app.route("/sign_in", methods=['POST'])
def sign_in():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)

    if not username:
        return make_error(400, 'Username is required')
    if not password:
        return make_error(400, 'Password is required')
    if len(username) > User.max_username_length:
        return make_error(400, 'Username length must be less than ' + str(
            User.max_username_length) + ' characters')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_error(400, 'This username is not exists')
    if not check_password_hash(user.password, password):
        return make_error(400, 'The password is incorrect')

    auth_token = generate_auth_token()
    user.auth_token = auth_token
    db.session.commit()

    response = jsonify(user.serialize())
    response.headers['X-Token'] = auth_token
    return response


def generate_auth_token():
    key = str(random.uniform(587329, 4832127819))
    value = str(datetime.datetime.now())
    auth_token_bytes = jwt.encode({key: value}, app.config.get('SECRET'),
                                  algorithm='HS256')

    return str(auth_token_bytes)


def validate_session(fn):
    @wraps(fn)
    def inner():
        authorized = validate_auth_token()
        if not authorized:
            return make_error(401, "User not authorized")
        else:
            return fn()

    return inner


def validate_auth_token():
    try:
        request_auth_token = request.headers['X-Token']
        user = User.query.filter_by(auth_token=request_auth_token).first()
        if user:
            return True
        else:
            raise ValueError('Wrong token')
    except (KeyError, ValueError):
        return False


@app.route("/castles", methods=['GET'])
@validate_session
def get_castles():
    castles = Castle.query.all()
    return jsonify(castles=[castle.serialize() for castle in castles])


@app.route("/units", methods=['GET'])
@validate_session
def get_units():
    castle_id = request.args.get('castle_id', type=int)
    units = Unit.query.filter(Unit.castle_id == castle_id).outerjoin(
        Unit.skills).all()
    return jsonify(units=[unit.serialize() for unit in units])


def make_error(code, message):
    error = jsonify({
        'details': message
    })
    error.status_code = code
    return error
