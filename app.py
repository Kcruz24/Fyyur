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
from datetime import datetime
from sqlalchemy.orm import backref

from forms import *
from models import Artist, Venue, Show

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
    start_time = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, venue_fk: {self.venue_fk1}, artist_fk: {self.artist_fk2}, start_time: {self.start_time}"


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(String), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)
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
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=True)
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
    #       num_shows should be aggregated based on number of upcoming shows per venue. (DONE)

    places = Venue.query.distinct(Venue.city, Venue.state).all()
    all_venues = Venue.query.all()

    data = []
    show_venues = []

    for place in places:
        for venue in all_venues:
            if venue.city == place.city and venue.state == place.state:
                show_venues.append({
                    "id": venue.id,
                    "name": venue.name,
                    "city": venue.city,
                    "state": venue.state,
                    "num_upcoming_shows": Show.query.join(Venue).filter(
                        venue.id == Show.venue_fk1 and Show.start_time > datetime.now()
                    ).count()
                })

        data.append({
            "city": place.city,
            "state": place.state,
            "venues": show_venues
        })

    print("venues", show_venues)

    return render_template('pages/venues.html', areas=data, venues=show_venues)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (DONE)
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term')
    all_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = []
    upcoming_shows = []

    for venue in all_venues:
        get_artist_shows = Show.query.join(Venue).filter(venue.id == Show.venue_fk1).all()
        for show in get_artist_shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)

        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcoming_shows)
        })

        upcoming_shows.clear()

    count = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).count()
    response = {
        "count": count,
        "data": data
    }

    print(data)

    return render_template('pages/search_venues.html', search_term=search_term, venues=response)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id (DONE)

    get_venue = Venue.query.get(venue_id)
    past_shows = []
    upcoming_shows = []
    past_shows_info = []
    upcoming_shows_info = []

    for show in get_venue.shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    for past_show in past_shows:
        past_shows_info.append({
            "artist_id": Artist.query.get(past_show.artist_fk2).id,
            "artist_name": Artist.query.get(past_show.artist_fk2).name,
            "artist_image_link": Artist.query.get(past_show.artist_fk2).image_link,
            "start_time": str(past_show.start_time)
        })

    for upcoming_show in upcoming_shows:
        upcoming_shows_info.append({
            "artist_id": Artist.query.get(upcoming_show.artist_fk2).id,
            "artist_name": Artist.query.get(upcoming_show.artist_fk2).name,
            "artist_image_link": Artist.query.get(upcoming_show.artist_fk2).image_link,
            "start_time": str(upcoming_show.start_time)
        })

    data = {
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
        "image_link": get_venue.image_link,
        "past_shows": past_shows_info,
        "upcoming_shows": upcoming_shows_info,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

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
    get_artists = Artist.query.all()
    data = []

    for artist in get_artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (DONE)
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term')
    all_artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    upcoming_shows = []
    data = []

    for artist in all_artists:
        get_artist_shows = Show.query.join(Artist).filter(artist.id == Show.artist_fk2).all()
        for show in get_artist_shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)

        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(upcoming_shows)
        })

        upcoming_shows.clear()

    count = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).count()
    response = {
        "count": count,
        "data": data
    }

    print(data)

    return render_template('pages/search_artists.html', artists=response,
                           search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id (DONE)

    upcoming_shows = []
    upcoming_shows_info = []
    past_shows = []
    past_shows_info = []
    get_artist = Artist.query.get(artist_id)
    get_shows = Show.query.filter(Show.artist_fk2 == artist_id).all()

    for show in get_shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    for past_show in past_shows:
        past_shows_info.append({
            "venue_id": Venue.query.get(past_show.venue_fk1).id,
            "venue_name": Venue.query.get(past_show.venue_fk1).name,
            "venue_image_link": Venue.query.get(past_show.venue_fk1).image_link,
            "start_time": str(past_show.start_time)
        })

    for upcoming_show in upcoming_shows:
        past_shows_info.append({
            "venue_id": Venue.query.get(upcoming_show.venue_fk1).id,
            "venue_name": Venue.query.get(upcoming_show.venue_fk1).name,
            "venue_image_link": Venue.query.get(upcoming_show.venue_fk1).image_link,
            "start_time": str(upcoming_show.start_time)
        })

    data = {
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
        "image_link": get_artist.image_link,
        "past_shows": past_shows_info,
        "upcoming_shows": upcoming_shows_info,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm(request.form)
    get_artist = Artist.query.get(artist_id)

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
    #       num_shows should be aggregated based on number of upcoming shows per venue. (DONE)

    all_shows = Show.query.all()

    data = []

    for show in all_shows:
        data.append({
            "venue_id": Venue.query.get(show.venue_fk1).id,
            "venue_name": Venue.query.get(show.venue_fk1).name,
            "artist_id": Artist.query.get(show.artist_fk2).id,
            "artist_name": Artist.query.get(show.artist_fk2).name,
            "artist_image_link": Artist.query.get(show.artist_fk2).image_link,
            "start_time": str(show.start_time)
        })

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
