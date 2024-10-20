from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add User')
