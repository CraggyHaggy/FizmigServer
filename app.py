from flask import Flask
from models import db


class ReverseProxied(object):
    def __init__(self, wsgi_app):
        self.app = wsgi_app

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
app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'postgresql://%(user)s:@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from api_controller import *

if __name__ == '__main__':
    app.run()
