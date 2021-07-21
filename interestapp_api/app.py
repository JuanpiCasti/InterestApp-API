from flask import Flask
from interestapp_api.Models import Models
from interestapp_api.Schemas import Schemas


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/interest_app'

db = Models.cur
db.init_app(app)

ma = Schemas.ma
ma.init_app(app)


@app.route('/')
def index():
    print(Schemas.record.dump(Models.Record.query.first()))
    return 'hola'
