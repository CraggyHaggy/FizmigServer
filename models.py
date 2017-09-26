from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })


class Castle(BaseModel, db.Model):
    __tablename__ = 'castles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class Unit(BaseModel, db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    level = db.Column(db.Integer, nullable=False)
    is_upgraded = db.Column(db.Boolean, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    min_damage = db.Column(db.Integer, nullable=False)
    max_damage = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    castle_id = db.Column(db.Integer, db.ForeignKey('castle_id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'is_upgraded': self.is_upgraded,
            'attack': self.attack,
            'defense': self.defense,
            'min_damage': self.min_damage,
            'max_damage': self.max_damage,
            'health': self.health,
            'speed': self.speed,
            'castle_id': self.castle_id
        }
