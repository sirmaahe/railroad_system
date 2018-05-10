from pony.orm import *

db = Database()


class Person(db.Entity):
    name = Required(str)
    worker = Optional('Worker')
    passenger = Optional('Passenger')


class Worker(db.Entity):
    person = Required(Person)
    salary = Required(int)
    repairer = Optional('Repairer')
    line = Optional('Line')


class Repairer(db.Entity):
    specialization = Required(str)
    worker = Required(Worker)


class Passenger(db.Entity):
    person = Required(Person)
    train = Required(str)


class Machinery(db.Entity):
    model = Required(str)
    line = Optional('Line')


class Train(db.Entity):
    number = Required(str, unique=True)
    model = Required(str)
    ptrain = Optional('PassengerTrain')
    ftrain = Optional('FreightTrain')
    queue = Optional('Queue')
    line = Optional('Line')


class PassengerTrain(db.Entity):
    train = Required(Train)
    all_places = Required(int)
    occupied_places = Required(int)


class FreightTrain(db.Entity):
    train = Required(Train)
    load = Required(int)


class Queue(db.Entity):
    train = Required(Train)
    place = Required(int)


class Line(db.Entity):
    train = Optional(Train)
    workers = Set('Worker')
    machinery = Set('Machinery')


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def start():
    # t = Train(number='123213', model='dsfds')
    # PassengerTrain(train=t, all_places=10, occupied_places=1)
    # Queue(train=t, place=1)
    # t = Train(number='2323', model='dsfds')
    # PassengerTrain(train=t, all_places=10, occupied_places=1)
    # Queue(train=t, place=2)
    # t = Train(number='sdvw23', model='dsfds')
    # FreightTrain(train=t, load=10)
    # Queue(train=t, place=3)

    # p1 = Person(name='safsfsf')
    # p2 = Person(name='safsfsf')
    # p3 = Person(name='safsfsf')
    # Worker(person=p1, salary=234)
    # Worker(person=p2, salary=234)
    # w = Worker(person=p3, salary=234)
    # r = Repairer(worker=w, specialization='safsfsf')
    pass

# start()
