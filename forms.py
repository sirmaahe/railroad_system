from wtforms import Form, StringField, SelectField, validators
from pony.orm import select, db_session

from models import Line


class PassengerForm(Form):
    name = StringField('name', [validators.Length(min=4)])
    train = StringField('train', [validators.DataRequired()])


class QueueForm(Form):
    train_number = StringField('number', render_kw={'readonly': True})
    place = StringField('place', [validators.DataRequired()])


@db_session
def get_lines():
    start = [('', '')]
    start.extend(select((l.id, l.id) for l in Line))
    return start


class WorkerForm(Form):
    name = StringField('name', [validators.Length(min=4)])
    salary = StringField('salary', [validators.DataRequired()])
    specialization = StringField('specialization')
    line = SelectField('line', choices=get_lines())
