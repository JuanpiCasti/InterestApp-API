from flask_marshmallow import Marshmallow


ma = Marshmallow()


class Record(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'record_type', 'initial_capital',
                  'rate', 'number_of_periods', 'effective_rate', 'final_sum')


record = Record()