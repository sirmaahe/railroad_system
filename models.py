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
    line = Optional('Line')


class Passenger(db.Entity):
    person = Required(Person)
    train = Required(str)


class Machinery(db.Entity):
    model = Required(str)
    line = Optional('Line')


class Train(db.Entity):
    number = Required(str)
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
    repairers = Set('Repairer')
    machinery = Set('Machinery')
