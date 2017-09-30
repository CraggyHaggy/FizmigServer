from flask import Flask, jsonify, request
from models import Castle, Unit, db


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)


app.config['DEBUG'] = True
POSTGRES = {
    'user': 'fizmig',
    'db': 'fizmig',
    'host': 'postgres',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/castles", methods=['GET'])
def castles():
    return jsonify(castles=[castle.serialize() for castle in Castle.query.all()])


@app.route("/units", methods=['GET'])
def units():
    castle_id = request.args.get('castle_id', type=int)
    return jsonify(units=[unit.serialize() for unit in Unit.query.filter(Unit.castle_id == castle_id).all()])


if __name__ == '__main__':
    app.run()
