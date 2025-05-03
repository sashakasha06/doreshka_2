# api/resources.py
from flask_restful import Resource, abort, reqparse
from models import db, Person


def abort_if_person_not_found(person_id):
    person = Person.query.get(person_id)
    if not person:
        abort(404, message=f"Person {person_id} not found")
    return person


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help="Name cannot be blank!")
parser.add_argument('age', required=True, type=int, help="Age must be an integer!")
parser.add_argument('work', required=False)
parser.add_argument('city', required=False)


class PersonResource(Resource):
    def get(self, id):
        person = abort_if_person_not_found(id)
        return {'person': person.to_dict()}

    def delete(self, id):
        person = abort_if_person_not_found(id)
        db.session.delete(person)
        db.session.commit()
        return f'Пользователь с ID {id} succesfully deleted'

    def put(self, id):
        args = parser.parse_args()
        person = abort_if_person_not_found(id)

        person.name = args['name']
        person.age = args['age']
        person.work = args.get('work', person.work)
        person.city = args.get('city', person.city)  # Добавьте это

        db.session.commit()
        return {'person': person.to_dict()}


class PersonListResource(Resource):
    def get(self):
        persons = Person.query.all()
        return {'persons': [person.to_dict() for person in persons]}

    def post(self):
        args = parser.parse_args()
        try:
            new_person = Person(
                name=args['name'],
                age=args['age'],
                work=args.get('work', ''),
                city=args.get('city', '')  # Добавьте это
            )
            db.session.add(new_person)
            db.session.commit()
            return 'Запись успешно добавлена', 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))