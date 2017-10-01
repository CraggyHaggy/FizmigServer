from flask import url_for, request, jsonify
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

    def compose_image_url(self):
        if type(self) == Castle:
            clazz = "castle"
        else:
            clazz = "unit"
        return request.url_root[:-1] + url_for(
            'static', filename=clazz + "_" + str(self.id) + ".png")


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
            'imageUrl': self.compose_image_url()
        }


units_skills = db.Table('units_skills',
                        db.Column('unit_id', db.Integer,
                                  db.ForeignKey('units.id')),
                        db.Column('skill_id', db.Integer,
                                  db.ForeignKey('skills.id')))


class Unit(BaseModel, db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    is_upgraded = db.Column(db.Boolean, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    min_damage = db.Column(db.Integer, nullable=False)
    max_damage = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    castle_id = db.Column(db.Integer, db.ForeignKey('castle_id'))
    skills = db.relationship('Skill', backref=db.backref('units', lazy=True),
                             lazy='dynamic', secondary=units_skills)

    def serialize(self):
        json_skills = list()
        for skill in self.skills.all():
            json_skills.append(skill.serialize())

        # This logic doesn't work!!! Use temporary decision.
        # 'skills': jsonify(
        #     skills=[skill.serialize() for skill in self.skills.all()]),

        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'skills': json_skills,
            'is_upgraded': self.is_upgraded,
            'attack': self.attack,
            'defense': self.defense,
            'min_damage': self.min_damage,
            'max_damage': self.max_damage,
            'health': self.health,
            'speed': self.speed,
            'castle_id': self.castle_id,
            'imageUrl': self.compose_image_url()
        }


class Skill(BaseModel, db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
