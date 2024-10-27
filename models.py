from email.mime import image
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import pokebase as pb
from sqlalchemy.dialects.postgresql import JSON

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/icons/catch.png")
    header_image_url = db.Column(db.Text, default="/static/images/icons/catch.png")
    bio = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User()
        user.username = username
        user.email = email
        user.image_url = image_url
        user.password = hashed_pwd

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    abilities = db.Column(db.String, nullable=False)  # Store as comma-separated string
    types = db.Column(db.String, nullable=False)  # Store as comma-separated string
    sprite_url = db.Column(db.String)

    def get_abilities(self):
        return self.abilities.split(",")  # Convert back to list

    def get_types(self):
        return self.types.split(",")  # Convert back to list



class Favorites(db.Model):
    """Mapping for many Pokemon favorited by many different Users."""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct table reference
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)



