from flask import jsonify, request

from app import app
from models import Castle, Unit


@app.route("/castles", methods=['GET'])
def get_castles():
    castles = Castle.query.all()
    return jsonify(castles=[castle.serialize() for castle in castles])


@app.route("/units", methods=['GET'])
def get_units():
    castle_id = request.args.get('castle_id', type=int)
    units = Unit.query.filter(Unit.castle_id == castle_id).all()
    return jsonify(units=[unit.serialize() for unit in units])
