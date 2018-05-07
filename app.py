from flask import Flask, render_template, request, redirect
from pony.orm import db_session, commit

from models import *
from forms import PassengerForm


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@db_session
def main():
    queue = Queue.select()
    lines = [{
        'id': l[0],
        'train_number': l[1],
        'workers': l[2],
        'repairers': l[3],
        'machinery': l[4],
    } for l in select(
        (l.id, l.train.number, count(l.workers), count(l.repairers), count(l.machinery)) for l in Line
    )]
    return render_template('main.html', queue=queue, lines=lines)


@app.route('/trains', methods=['GET', 'POST'])
@db_session
def trains():
    trains = Train.select()
    return render_template('trains.html', trains=trains)


@app.route('/passengers/', methods=['GET', 'POST'])
@db_session
def passengers():
    passengers = Passenger.select()
    return render_template('passengers.html', passengers=passengers)


@app.route('/passengers/<passenger_id>/edit/', methods=['GET', 'POST'])
@db_session
def edit_passenger(passenger_id):
    passenger = Passenger[passenger_id]
    form = PassengerForm(request.form, data={'name': passenger.person.name, 'train': passenger.train})
    if request.method == 'POST' and form.validate():
        passenger.person.name = form.name.data
        passenger.train = form.train.data
        commit()
        return redirect('/passengers/')
    return render_template('edit_passenger.html', form=form)


if __name__ == "__main__":
    app.run()
