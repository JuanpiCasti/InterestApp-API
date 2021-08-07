from Models import connection, record
from Schemas import schemas, record_schema
from flask import Flask, jsonify, request


app = Flask(__name__)

#setup and shortcut sqlalchemy models and db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/interest_app'
db = connection.db
db.init_app(app)
record = record.Record 

#setup and shortcut marshmallow schemas
schemas.ma.init_app(app)
record_schema = record_schema.record

def calc_final_sum(capital, rate, time, type):
    if type == "anual":
        final_sum = capital*(1+rate)**time
    if type =="monthly":
        final_sum = capital*(1+(rate/12))**(time*12)
    if type == "weekly":
        final_sum = capital*(1+(rate/52))**(time*52)
    if type == "daily":
        final_sum = capital*(1+(rate/365))**(time*365)

@app.route('/', methods=['GET'])
def get_all():
    rows = record.query.all()
    row_arr = []
    for row in rows:
        row_arr.append(record_schema.dump(row))
    return jsonify(row_arr)

@app.route('/insert', methods=['POST'])
def insert_record():

    if request.method == 'POST':

        data = request.form.to_dict()

        effective_rate = float(data.get('effective_rate'))
        initial_capital = float(data.get('initial_capital'))
        name = data.get('name')[0:20]
        number_of_periods = int(data.get('number_of_periods'))
        rate = float(data.get('rate'))
        type = str(data.get('type'))

        final_sum = calc_final_sum(initial_capital, rate, number_of_periods,type)

        row = record(effective_rate, final_sum, initial_capital, name, number_of_periods, rate, type)
        db.session.add(row)
        db.session.commit()

        response_record = record.query.all()[-1]
        response = record_schema.dump(response_record)

        return response
    else:
        return {'error': 'Incorrect HTTP method'}

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    if request.method == 'DELETE':
        row = record.query.get(id)
        response_record = row
        db.session.delete(row)
        db.session.commit()
        response = record_schema.dump(response_record)
        return response
    else:
        return {'error': 'Incorrect HTTP method'}

@app.route('/edit/<int:id>', methods=['PUT'])
def edit_record(id):
    if request.method == 'PUT':
        row = record.query.get(id)
        request_dict = request.form.to_dict()
        row.name = request_dict.get('name')
        row.initial_capital = request_dict.get('initial_capital')
        row.rate = request_dict.get('rate')
        row.number_of_periods = request_dict.get('number_of_periods')
        row.effective_rate = request_dict.get('effective_rate')
        row.final_sum = request_dict.get('final_sum')

        db.session.commit()

        new_row = record.query.get(id)
        response = record_schema.dump(new_row)
        return response
    else:
        return {'error': 'Incorrect HTTP method'}


if __name__ == "__main__":
    app.run(debug=True)