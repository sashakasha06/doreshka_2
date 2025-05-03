# app.py
from flask import Flask, render_template
from flask_restful import Api
from models import db, Person
# from ucebnik_2.tmp.routes import api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GEOCODER_API_KEY'] = 'ce605fe0-4a25-4c96-ae17-a0e299033316'
app.config['MAPS_API_KEY'] = '3d75ebfa-8eae-4faa-b57f-53f50480cbd8'

# Инициализация БД
db.init_app(app)

# Инициализация Flask-RESTful
api = Api(app)

# Создаём таблицы вручную
with app.app_context():
    db.create_all()

# Регистрация Blueprint (если вам еще нужно сохранить старые маршруты)
# app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    people = Person.query.all()
    return render_template('home.html', people=people)

# Добавляем ресурсы Flask-RESTful
from api.resources import PersonResource, PersonListResource
api.add_resource(PersonListResource, '/api/v2/persons')
api.add_resource(PersonResource, '/api/v2/persons/<int:id>')

@app.route('/users_show/<int:user_id>')
def user_show(user_id):
    person = Person.query.get_or_404(user_id)
    return render_template('user_show.html',
                         person=person,
                         geocoder_key=app.config['GEOCODER_API_KEY'],
                         maps_key=app.config['MAPS_API_KEY'])


def init_test_data():
    with app.app_context():
        # Проверяем, есть ли уже записи в базе
        if Person.query.count() == 0:
            test_persons = [
                Person(name='Иван Петров', age=28, work='Разработчик', city='Москва'),
                Person(name='Анна Сидорова', age=32, work='Дизайнер', city='Санкт-Петербург'),
                Person(name='Сергей Иванов', age=45, work='Менеджер', city='Казань'),
                Person(name='Елена Смирнова', age=23, work='Аналитик', city='Новосибирск')
            ]

            db.session.bulk_save_objects(test_persons)
            db.session.commit()
            print("Добавлены тестовые данные")

if __name__ == '__main__':
    init_test_data()
    app.run(debug=True)