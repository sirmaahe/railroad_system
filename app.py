from flask import Flask, render_template, request, redirect
from pony.orm import db_session, commit

from models import *
from forms import PassengerForm, QueueForm, WorkerForm


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@db_session
def main():
    queue = Queue.select()
    lines = [{
        'id': l[0],
        'train_number': l[1],
        'workers': l[2],
        'machinery': l[3],
    } for l in select(
        (l.id, l.train.number, count(l.workers), count(l.machinery)) for l in Line
    )]
    return render_template('main.html', queue=queue, lines=lines)


@app.route('/trains/', methods=['GET', 'POST'])
@db_session
def trains():
    trains = Train.select()
    return render_template('trains.html', trains=trains)


@app.route('/passengers/', methods=['GET', 'POST'])
@db_session
def passengers():
    passengers = Passenger.select()
    return render_template('passengers.html', passengers=passengers)


@app.route('/workers/', methods=['GET', 'POST'])
@db_session
def workers():
    workers = Worker.select()
    return render_template('workers.html', workers=workers)


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


@app.route('/workers/<worker_id>/edit/', methods=['GET', 'POST'])
@db_session
def edit_worker(worker_id):
    worker = Worker[worker_id]
    repairer = worker.repairer
    form = WorkerForm(request.form, data={
        'name': worker.person.name,
        'salary': worker.salary,
        'specialization': repairer.specialization if repairer else '',
        'line': worker.line,
    })
    if request.method == 'POST' and form.validate():
        worker.person.name = form.name.data
        worker.salary = form.salary.data

        if form.line.data:
            worker.line = Line[form.line.data] if form.line.data else None

        specialization = form.specialization.data
        if form.specialization.data:
            if not repairer:
                Repairer(worker=worker, specialization=specialization)
            else:
                worker.specialization = specialization
        commit()
        return redirect('/workers/')
    return render_template('edit_worker.html', form=form)


@app.route('/queue/<queue_id>/edit/', methods=['GET', 'POST'])
@db_session
def edit_queue(queue_id):
    queue = Queue[queue_id]
    form = QueueForm(request.form, data={'train_number': queue.train.number, 'place': queue.place})
    if request.method == 'POST' and form.validate():
        another_queue = Queue.get(place=form.place.data)
        if another_queue:
            another_queue.place = queue.place
        commit()

        queue.place = form.place.data
        commit()
        return redirect('/')
    return render_template('edit_queue.html', form=form)


if __name__ == "__main__":
    app.run()
