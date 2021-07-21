from flask_sqlalchemy import SQLAlchemy

cur = SQLAlchemy()
hola = 'hola'

class Record(cur.Model):
    id = cur.Column(cur.Integer, primary_key=True)
    name = cur.Column(cur.String(20))
    record_type = cur.Column(cur.String(10))
    initial_capital = cur.Column(cur.Float)
    rate = cur.Column(cur.Float)
    number_of_periods = cur.Column(cur.Integer)
    effective_rate = cur.Column(cur.Float)
    final_sum = cur.Column(cur.Float)

    def __repr__(self):
        return f"This is {self.name}."
