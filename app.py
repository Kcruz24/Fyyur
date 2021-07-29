# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import sys

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from sqlalchemy import String, func

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# TODO: connect to a local postgresql database (DONE)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
class Show(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    venue_fk1 = db.Column(db.Integer(), db.ForeignKey('venue.id'), nullable=False)
    artist_fk2 = db.Column(db.Integer(), db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, venue_fk: {self.venue_fk1}, artist_fk: {self.artist_fk2}, start_time: {self.start_time}"


# TODO: Set genres column in Artist and Venue to False, check psql

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(String), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True, unique=True)
    image_link = db.Column(db.String(500), nullable=False, unique=True)
    website_link = db.Column(db.String(500), nullable=False, unique=True)
    seeking_talent = db.Column(db.Boolean(), nullable=True, default=False)
    seeking_description = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f"Table id: {self.id}, name: {self.name}"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (DONE)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(String), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True, unique=True)
    image_link = db.Column(db.String(500), nullable=False, unique=True)
    website_link = db.Column(db.String(500), nullable=True, unique=True)
    seeking_venues = db.Column(db.Boolean(), nullable=True, default=False)
    seeking_description = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, " \
               f"phone: {self.phone}, genres: {self.genres}, facebook_link: {self.facebook_link}, " \
               f"image_link: {self.image_link}, website_link: {self.website_link}, seeking_venues: {self.seeking_venues}, " \
               f"seeking_description: {self.seeking_description}"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (DONE)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. (DONE)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    #       FALTA: falta lo de los num_shows (Partially DONE)

    places = Venue.query.distinct(Venue.city, Venue.state).all()
    all_venues = Venue.query.all()

    # print(localAreas)
    # print(localAreas[0].get("city"))
    # print(localAreas[0].get("venues"))
    # print(localAreas[0].get("venues")[0].get("name"))
    # data = [{
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "venues": [{
    #         "id": 1,
    #         "name": "The Musical Hop",
    #         "num_upcoming_shows": 0,
    #     }, {
    #         "id": 3,
    #         "name": "Park Square Live Music & Coffee",
    #         "num_upcoming_shows": 1,
    #     }]
    # }, {
    #     "city": "New York",
    #     "state": "NY",
    #     "venues": [{
    #         "id": 2,
    #         "name": "The Dueling Pianos Bar",
    #         "num_upcoming_shows": 0,
    #     }]
    # }]

    return render_template('pages/venues.html', areas=places, venues=all_venues)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (DONE)
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term')
    all_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    count = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).count()

    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 2,
    #         "name": "The Dueling Pianos Bar",
    #         "num_upcoming_shows": 0,
    #     }]
    # }

    return render_template('pages/search_venues.html', search_term=search_term, venues=all_venues, count=count)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    #       FALTA: Lo de past_shows, upcoming_shows, past_shows_count, y upcoming_shows_count (Partially DONE)
    data1 = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid"
                      "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [{
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid"
                                 "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid"
                      "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid"
                      "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "past_shows": [{
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid"
                                 "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [{
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                                 "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                                 "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                                 "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 1,
        "upcoming_shows_count": 1,
    }
    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

    data = Venue.query.get(venue_id)

    print(f"Genres: {data.genres}")

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead (DONE)
    error = False

    form = VenueForm(request.form)

    print(request.values)
    print(request.args)
    print("Form genres:", form.genres.data)
    try:
        req_name = form.name.data
        req_city = form.city.data
        req_state = form.state.data
        req_address = form.address.data
        req_phone = form.phone.data
        req_genres = form.genres.data
        req_facebook_link = form.facebook_link.data
        req_image_link = form.image_link.data
        req_website_link = form.website_link.data

        req_seeking_talent = False
        if form.seeking_talent.data == "y":
            req_seeking_talent = True

        req_seeking_description = form.seeking_description.data

        new_venue = Venue(name=req_name, city=req_city, state=req_state, address=req_address, phone=req_phone,
                          genres=req_genres, facebook_link=req_facebook_link, image_link=req_image_link,
                          website_link=req_website_link, seeking_talent=req_seeking_talent,
                          seeking_description=req_seeking_description)

        db.session.add(new_venue)
        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except():
        db.session.rollback()
        flash('An error occurred. Venue could not be listed.')
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return render_template('pages/home.html')
    else:
        abort(500)

    # TODO: modify data to be the data object returned from db insertion (DONE)
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. (DONE)
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    #       SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail. (DONE)
    error = False

    try:
        venue_to_delete = Venue.query.get(venue_id)
        flash("Successfully deleted " + venue_to_delete.name + ".")
        db.session.delete(venue_to_delete)
        db.session.commit()
    except():
        db.session.rollback()
        flash("Could not delete " + Venue.query.get(venue_id).name + ".")
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # TODO: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    #       clicking that button delete it from the db then redirect the user to the homepage (DONE)

    if not error:
        return redirect(url_for("index"))
    else:
        abort(500)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database (DONE)
    data = Artist.query.all()

    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (DONE)
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term')
    all_artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    count = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).count()

    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 4,
    #         "name": "Guns N Petals",
    #         "num_upcoming_shows": 0,
    #     }]
    # }
    return render_template('pages/search_artists.html', artists=all_artists, count=count,
                           search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id (Partially DONE)
    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid"
    #                   "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [{
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid"
    #                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    #     "genres": ["Jazz"],
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "300-400-5000",
    #     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid"
    #                   "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "past_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid"
    #                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    #     "genres": ["Jazz", "Classical"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "432-325-5432",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
    #                   "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid"
    #                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid"
    #                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid"
    #                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

    data = Artist.query.get(artist_id)

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm(request.form)
    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid"
    #                   "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80 "
    # }

    get_artist = Artist.query.get(artist_id)
    print(f"Artist: {get_artist}")
    print(f"Id: {get_artist.id}")
    print(f"Form name: {get_artist.name}")
    print(f"Website link: {get_artist.website_link}")
    artist = {
        "id": get_artist.id,
        "name": get_artist.name,
        "genres": get_artist.genres,
        "city": get_artist.city,
        "state": get_artist.state,
        "phone": get_artist.phone,
        "website": get_artist.website_link,
        "facebook_link": get_artist.facebook_link,
        "seeking_venue": get_artist.seeking_venues,
        "seeking_description": get_artist.seeking_description,
        "image_link": get_artist.image_link
    }

    # TODO: populate form with fields from artist with ID <artist_id> (DONE)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing (DONE)
    # artist record with ID <artist_id> using the new attributes
    error = False
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)

    print(request.values)
    print(f"Form {form}")
    try:
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website_link = form.website_link.data
        artist.seeking_venues = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f"Artist {artist.name} was successfully edited!")
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash(f"Could not edit {artist.name} :(")
    finally:
        db.session.close()

    if not error:
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        abort(500)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # venue = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid"
    #                   "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60 "
    # }

    get_venue = Venue.query.get(venue_id)

    venue = {
        "id": get_venue.id,
        "name": get_venue.name,
        "genres": get_venue.genres,
        "address": get_venue.address,
        "city": get_venue.city,
        "state": get_venue.state,
        "phone": get_venue.phone,
        "website": get_venue.website_link,
        "facebook_link": get_venue.facebook_link,
        "seeking_talent": get_venue.seeking_talent,
        "seeking_description": get_venue.seeking_description,
        "image_link": get_venue.image_link
    }

    # TODO: populate form with values from venue with ID <venue_id> (DONE)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing (DONE)
    # venue record with ID <venue_id> using the new attributes

    error = False
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)

    print(request.values)
    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.website_link = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f"Successfully edited {venue.name}!")
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash(f"Something went wrong editing {venue.name}")
    finally:
        db.session.close()

    if not error:
        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        abort(500)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead (DONE)
    # TODO: modify data to be the data object returned from db insertion (DONE)
    error = False

    form = ArtistForm(request.form)

    print(request.values)
    print(request.args)
    try:
        req_name = form.name.data
        req_city = form.city.data
        req_state = form.state.data
        req_phone = form.phone.data
        req_genres = form.genres.data
        req_facebook_link = form.facebook_link.data
        req_image_link = form.image_link.data
        req_website_link = form.website_link.data

        req_seeking_venues = False
        if form.seeking_venue.data == "y":
            req_seeking_venues = True

        req_seeking_description = form.seeking_description.data

        new_artist = Artist(name=req_name, city=req_city, state=req_state, phone=req_phone,
                            genres=req_genres, facebook_link=req_facebook_link, image_link=req_image_link,
                            website_link=req_website_link, seeking_venues=req_seeking_venues,
                            seeking_description=req_seeking_description)

        db.session.add(new_artist)
        db.session.commit()
        flash('Artist ' + req_name + ' was successfully listed!')
    except():
        flash('Artist could not be listed :(')
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return render_template('pages/home.html')
    else:
        abort(500)
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. (DONE)
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # Attempt to query from the associative show table
    show_record = Venue.query.join(show).join(Artist).filter(
        (show.c.venue_id == Venue.id) & (show.c.artist_id == Artist.id)
    ).all()

    print("Show record: ", show_record)

    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid"
                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid"
                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid"
                             "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead (DONE)
    # on successful db insert, flash success
    print(request.values)

    error = False
    form = ShowForm(request.form)

    try:
        req_venue_id = form.venue_id.data
        req_artist_id = form.artist_id.data
        req_start_time = form.start_time.data

        new_show = Show(venue_fk1=req_venue_id, artist_fk2=req_artist_id, start_time=req_start_time)
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash("Something went wrong when trying to list a show! :(")
    finally:
        db.session.close()

    if not error:
        return render_template('pages/home.html')
    else:
        abort(500)

    # TODO: on unsuccessful db insert, flash an error instead. (DONE)
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
