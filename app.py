import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from models import Favorites, User, Pokemon, db, pb
from forms import UserAddForm, LoginForm, UserForm

load_dotenv()
#API Info
# The 'pb' from models will be our main easy way to communicate with the api following the 
# Suggestions of the API creators. This way all python files can use it.

#User 
CURR_USER_KEY = "curr_user"

app = Flask(__name__)

def create_app():
    """Factory function to create Flask application and initialize extensions."""
    

    # Configure database using environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy event warnings
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

# Create the application instance

# For local debugging (not for production)



##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have logged out successfully", "success")
    return redirect("/")

@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserForm(obj=user)

    if form.validate_on_submit():
        # User needs to enter password to authenticate

        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.header_image_url = form.header_image_url.data
            user.bio = form.bio.data

            db.session.commit()
            flash("Profile updated", "success")
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again", "danger")

    return render_template("users/edit.html", form=form)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    template = 'home-anon.html'
    pokemon_data = basicpokedata('blastoise')


    # if g.user: will set correct homepage for base
    if g.user:
        template = 'home.html'
        favorites_list = (db.session.query(Pokemon)
            .join(Favorites, Favorites.pokemon_id == Pokemon.id)
            .filter(Favorites.user_id == g.user.id)
            .order_by(Pokemon.id)  # Add this line to order by Pokémon ID
            .all())
        
        if favorites_list:
            pokemonlst = []
            for id in favorites_list:
                pokemon = basicpokedata(id.name)
                pokemonlst.append(pokemon)
            return render_template(template, pokemonlst=pokemonlst)
        
        return render_template(template)


    # Fetching data about a specific Pokémon (e.g., Pikachu)
    pokemon_data = basicpokedata('blastoise')

    return render_template(template, pokemon=pokemon_data)

@app.route('/pokemon-info')
def pokemon_info():
    """Handle info page for a pokémon."""
    pokemon_name = request.args.get('pokemon_name', None)
    

    if pokemon_name:
        pokemon_data = allpokedata(pokemon_name)

        if pokemon_data:
            return render_template('pokemon-info.html', pokemon = pokemon_data)
        
    flash(f"Invalid Pokémon name or ID. Please try again. {pokemon_name}", "danger")
    return redirect("/")
    

@app.route('/pokemon-caught')
def add_to_caught():
    """Capture Pokémon and add it to favorites, then display all favorites."""
    pokemon_name = request.args.get('pokemon_name', None)

    if not g.user:
        flash('You need to sign in first', 'danger')
        return redirect("/signup")

    if pokemon_name:


        try:
            # Fetch Pokémon data either from the database or Pokebase
            pokemon_data = basicpokedata(pokemon_name)
        except Exception as e:
            flash(f"Error fetching Pokémon data: {e}", "danger")
            return redirect('/')

        # Check if Pokémon is already in the favorites list
        existing_favorite = Favorites.query.filter_by(user_id=g.user.id, pokemon_id=pokemon_data['id']).first()
        if existing_favorite:
            flash(f"{pokemon_name.capitalize()} is already in your favorites!", "warning")
        else:
            # Add the favorite to the database
            favorite = Favorites()
            favorite.user_id=g.user.id, 
            favorite.pokemon_id=pokemon_data['id']
            db.session.add(favorite)
            db.session.commit()

            flash(f"{pokemon_name.capitalize()} has been added to your favorites!", "success")

        # Display the caught Pokémon's data
        return render_template('pokemon-caught.html', pokemon=pokemon_data)

    flash(f"Failed to catch {pokemon_name}. Please try again.", "danger")
    return redirect('/')





##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

#Helper Methods so as to not have to repeat these process
def basicpokedata(name):
    # Step 1: Check if the Pokémon exists in the database first
    pokemon = Pokemon.query.filter_by(name=name).first()

    if pokemon:
        return {
            'id': pokemon.id,
            'name': pokemon.name,
            'abilities': pokemon.get_abilities(),  # This assumes a method for splitting abilities string
            'types': pokemon.get_types(),  # This assumes a method for splitting types string
            'sprite': pokemon.sprite_url
        }
    
    # Fetch Pokémon data from Pokébase
    pokemon = pb.pokemon(name.lower())
    # Extracting useful information
    abilities = [ability.ability.name for ability in pokemon.abilities]
    types = [poke_type.type.name for poke_type in pokemon.types]

    pokemon_data = {
        'id': pokemon.id,
        'name': pokemon.name,
        'abilities': abilities,
        'types': types,
        'sprite': pokemon.sprites.front_default
    }

    try:

        # Step 2: Add new Pokémon to the database if it doesn't already exist
        new_pokemon = Pokemon()
        new_pokemon.id=pokemon.id,
        new_pokemon.name=pokemon.name,
        new_pokemon.abilities=",".join(abilities),  # Convert list to comma-separated string
        new_pokemon.types=",".join(types),  # Convert list to comma-separated string
        new_pokemon.sprite_url=pokemon.sprites.front_default
        

        # Add the new Pokémon to the database
        db.session.add(new_pokemon)
        db.session.commit()

        return pokemon_data

    except Exception as e:
        db.session.rollback()  # Rollback in case of any failure
        flash(f"Error fetching Pokémon data: {e}", "danger")
        return pokemon_data

    
def allpokedata(name):
    try:
        pokemon = pb.pokemon(name.lower())
        speciesdata = pb.pokemon_species(name.lower())

        # Extracting useful information
        pokemon_data = {
            'id': pokemon.id,
            'name': pokemon.name,
            'heightdm': pokemon.height,
            'heightcm': (pokemon.height * 10),
            'heightft': round(pokemon.height * 0.328084, 2),
            'weighthg': pokemon.weight,
            'weightkg': round(pokemon.weight * 0.1, 1),
            'weightlb': round(pokemon.weight * 0.220462, 1),
            'abilities': get_pokemon_abilities_with_effects(pokemon),
            'types': [poke_type.type.name for poke_type in pokemon.types],
            'sprite': pokemon.sprites.front_default,
            'flavortext': speciesdata.flavor_text_entries[0].flavor_text
        }
        return pokemon_data
    except Exception as e:
        return flash(f"Error fetching Pokémon data: {e}")
    
def get_pokemon_abilities_with_effects(pokemon):
    """Fetch abilities and their effects for a given Pokémon."""
    abilities = []

    for ability_info in pokemon.abilities:
        ability_name = ability_info.ability.name
        ability_data = pb.ability(ability_name)  # Fetch ability data to get effect

        # Find the English effect description
        ability_effect = next(
            (effect.effect for effect in ability_data.effect_entries if effect.language.name == 'en'), 
            "No English description available."
        )

        abilities.append({
            'name': ability_name,
            'effect': ability_effect
        })

    return abilities


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)