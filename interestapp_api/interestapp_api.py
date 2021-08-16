from os import error
from Models import connection, record
from Schemas import schemas, record_schema
from flask import Flask, jsonify, request

#TODO calculate effective rate

app = Flask(__name__)

#setup and shortcut sqlalchemy models and db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///interestapp.db'
db = connection.db
db.init_app(app)
record = record.Record 

#setup and shortcut marshmallow schemas
schemas.ma.init_app(app)
record_schema = record_schema.record

def calc_final_sum(capital, rate, time, type_of_period):
    rate = rate/100
    if type_of_period == "annual":
        final_sum = capital*((1+rate)**time)
    elif type_of_period =="monthly":
        final_sum = capital*((1+(rate/12))**(time*12))
    elif type_of_period == "weekly":
        final_sum = capital*((1+(rate/52))**(time*52))
    elif type_of_period == "daily":
        final_sum = capital*((1+(rate/365))**(time*365))
    return final_sum


def correct_input_data(data):
        clean_data = {
            'initial_capital' : float(data.get('initial_capital', False)),
            'name' : data.get('name', False)[0:20],
            'number_of_periods' : int(data.get('number_of_periods', False)),
            'rate' : float(data.get('rate', False)),
            'type_of_period' : data.get('type_of_period', False)
        }

        return clean_data

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
        input_values =  correct_input_data(data)

        missing = []

        for key in input_values.keys():
            if not input_values[key]:
                missing.append(key)
        
        if not missing:

            
            if input_values['type_of_period'] in ['annual', 'monthly','weekly','daily']:
                final_sum = calc_final_sum(input_values['initial_capital'], input_values['rate'], input_values['number_of_periods'],input_values['type_of_period'])
            else:
                return {'error': "type_of_period has an incorrect value, it should be 'annual', 'monthly', 'weekly' or 'daily' "}

            row = record(final_sum=final_sum, initial_capital=input_values['initial_capital'], name=input_values['name'], number_of_periods=input_values['number_of_periods'], rate=input_values['rate'], type_of_period=input_values['type_of_period'])
            db.session.add(row)
            db.session.commit()
            id = row.id
            
            response_record = record.query.get(id)
            response = record_schema.dump(response_record)
    
            return response
        else:
            response = {}
            error = ''
            for el in missing:
                error += el + ', '
            response['error'] = error + 'is/are missing.'
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
        data = request.form.to_dict()
        input_values = correct_input_data(data)
        missing = []

        for key in input_values.keys():
            if not input_values[key]:
                missing.append(key)
        
        if not missing:

            if input_values['type_of_period'] in ['annual', 'monthly','weekly','daily']:
                row.final_sum = calc_final_sum(input_values['initial_capital'], input_values['rate'], input_values['number_of_periods'],input_values['type_of_period'])
            else:
                return {'error': "type_of_period has an incorrect value, it should be 'annual', 'monthly', 'weekly' or 'daily' "}
            row.initial_capital = input_values['initial_capital']
            row.name = input_values['name']
            row.number_of_periods = input_values['number_of_periods']
            row.rate = input_values['rate']
            row.type_of_period = input_values['type_of_period']

            db.session.commit()

            response = record_schema.dump(row)
            return response
            
        else:
            response = {}
            error = ''
            for el in missing:
                error += el + ', '
            response['error'] = error + 'is/are missing.'
            return response
    else:
        return {'error': 'Incorrect HTTP method'}


if __name__ == "__main__":
    app.run()