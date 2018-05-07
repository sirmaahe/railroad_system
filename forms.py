from wtforms import Form, StringField, validators


class PassengerForm(Form):
    name = StringField('name', [validators.Length(min=4)])
    train = StringField('train', [validators.DataRequired()])
