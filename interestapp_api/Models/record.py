from flask_sqlalchemy import SQLAlchemy
from . import connection
db = connection.db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    initial_capital = db.Column(db.Float)
    rate = db.Column(db.Float)
    number_of_periods = db.Column(db.Integer)
    final_sum = db.Column(db.Float)
    type_of_period = db.Column(db.String(10))

    def __repr__(self):
        return f"This is record id {self.id}."
