from flask_sqlalchemy import SQLAlchemy
from . import connection
db = connection.db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    initial_capital = db.Column(db.Float)
    rate = db.Column(db.Float)
    number_of_periods = db.Column(db.Integer)
    effective_rate = db.Column(db.Float)
    final_sum = db.Column(db.Float)
    type = db.Column(db.String(10))

    def __init__(self, effective_rate, final_sum, initial_capital, name, number_of_periods, rate, type):
        self.effective_rate = effective_rate
        self.final_sum = final_sum
        self.initial_capital = initial_capital
        self.name = name
        self.number_of_periods = number_of_periods
        self.rate = rate
        self.type = type

    def __repr__(self):
        return f"This is record number {self.name}."
