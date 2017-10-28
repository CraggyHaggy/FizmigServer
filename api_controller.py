from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from models import Castle, Unit, User, db


# TODO: authorization logic
# (Implement SignOut, Tokens, Multiple errors).

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

    response = jsonify(user.serialize())
    response.headers['X-Token'] = 'KALYAN, GDE IMPLEMENTACIYA!!!!!!'
    return response


@app.route("/castles", methods=['GET'])
def get_castles():
    castles = Castle.query.all()
    return jsonify(castles=[castle.serialize() for castle in castles])


@app.route("/units", methods=['GET'])
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
