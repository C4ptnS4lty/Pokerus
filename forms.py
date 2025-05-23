from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from models import User, Pokemon, Favorites, pb

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    #Need to perfect this, probabl use image_url of small pokemon sprite
    image_url = StringField('Image URL') #Jon you idiot, need to add this to signup


class UserForm(FlaskForm):
    """Form for editing user information."""

    username = StringField('Username')
    email = StringField('E-mail')
    image_url = StringField('Image URL')
    header_image_url = StringField('Image URL')
    bio = StringField('Bio', )
    password = PasswordField('Password')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

    
    