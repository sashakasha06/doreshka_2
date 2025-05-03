from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from models import Category  # Добавляем импорт модели

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddWorkForm(FlaskForm):
    description = TextAreaField('Описание работы', validators=[DataRequired()])
    categories = SelectMultipleField(
        'Категории',
        coerce=int,
        validators=[DataRequired(message="Пожалуйста, выберите хотя бы одну категорию")]
    )
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(AddWorkForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(c.id, c.name) for c in Category.query.all()]