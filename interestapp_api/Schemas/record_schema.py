from . import schemas

ma = schemas.ma

class Record(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'initial_capital',
                  'rate', 'number_of_periods', 'final_sum', 'type')


record = Record()
records = Record(many=True)
