from Models import connection, record
from Schemas import schemas, record_schema
from flask import Flask


app = Flask(__name__)

#setup and shortcut sqlalchemy models and db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/interest_app'
db = connection.db
db.init_app(app)
record = record.Record 

#setup and shortcut marshmallow schemas
schemas.ma.init_app(app)
record_schema = record_schema.record


@app.route('/')
def index():
    print(record_schema.dump(record.query.first()))
    return 'pedo'


if __name__ == "__main":
    app.run(debug=True)
