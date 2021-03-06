# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys
import babel
import logging
import dateutil.parser

from forms import *
from logging import Formatter, FileHandler
from models import Artist, Venue, Show, db, app
from flask import render_template, request, flash, redirect, url_for, abort


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM dd, y h:mma"
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
    #       num_shows should be aggregated based on number of
    #       upcoming shows per venue. (DONE)

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
                    "num_upcoming_shows":
                        len([show for show in venue.shows
                             if show.start_time > datetime.now()])
                })

        data.append({
            "city": place.city,
            "state": place.state
        })

    print("venues", show_venues)

    return render_template('pages/venues.html', areas=data, venues=show_venues)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search.
    #       Ensure it is case-insensitive. (DONE)
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and
    # "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term')
    all_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = []
    upcoming_shows = []

    for venue in all_venues:
        for show in venue.shows:
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

    return render_template('pages/search_venues.html',
                           search_term=search_term,
                           venues=response)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table,
    #       using venue_id (DONE)

    get_venue = Venue.query.get_or_404(venue_id)
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
            "artist_id": Artist.query.get_or_404(past_show.artist_id).id,
            "artist_name": Artist.query.get_or_404(past_show.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
                past_show.artist_id).image_link,
            "start_time": str(past_show.start_time)
        })

    for upcoming_show in upcoming_shows:
        upcoming_shows_info.append({
            "artist_id": Artist.query.get_or_404(upcoming_show.artist_id).id,
            "artist_name": Artist.query.get_or_404(
                upcoming_show.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
                upcoming_show.artist_id).image_link,
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

    if form.validate_on_submit():
        try:
            new_venue = Venue()
            form.populate_obj(new_venue)

            db.session.add(new_venue)
            db.session.commit()

            flash(f'Venue {form.name.data} was successfully listed!')
        except():
            db.session.rollback()
            flash('An error occurred. Venue could not be listed.')
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash(f"Errors: {message}")

    if not error:
        return render_template('pages/home.html')
    else:
        abort(500)

    # TODO: modify data to be the data object returned from db insertion (DONE)
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. (DONE)
    # e.g.,
    # flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    #       SQLAlchemy ORM to delete a record. Handle cases where
    #       the session commit could fail. (DONE)
    error = False

    try:
        venue_to_delete = Venue.query.get_or_404(venue_id)
        db.session.delete(venue_to_delete)
        db.session.commit()
        flash("Successfully deleted " + venue_to_delete.name + ".")
    except():
        db.session.rollback()
        flash("Could not delete " + Venue.query.get_or_404(venue_id).name + ".")
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # TODO: BONUS CHALLENGE: Implement a button to delete a Venue on a
    #       Venue Page, have it so that clicking that button delete it from
    #       the db then redirect the user to the homepage (DONE)

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
    # TODO: implement search on artists with partial string search.
    #       Ensure it is case-insensitive. (DONE)
    # seach for "A" should return "Guns N Petals", "Matt Quevado",
    # and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term')
    all_artists = Artist.query.filter(
        Artist.name.ilike(f'%{search_term}%')).all()
    upcoming_shows = []
    data = []

    for artist in all_artists:
        for show in artist.shows:
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
    # TODO: replace with real artist data from the artist table,
    #       using artist_id (DONE)

    upcoming_shows = []
    upcoming_shows_info = []
    past_shows = []
    past_shows_info = []
    get_artist = Artist.query.get_or_404(artist_id)

    for show in get_artist.shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    for past_show in past_shows:
        past_shows_info.append({
            "venue_id": Venue.query.get_or_404(past_show.venue_id).id,
            "venue_name": Venue.query.get_or_404(past_show.venue_id).name,
            "venue_image_link": Venue.query.get_or_404(
                past_show.venue_id).image_link,
            "start_time": str(past_show.start_time)
        })

    for upcoming_show in upcoming_shows:
        upcoming_shows_info.append({
            "venue_id": Venue.query.get_or_404(upcoming_show.venue_id).id,
            "venue_name": Venue.query.get_or_404(upcoming_show.venue_id).name,
            "venue_image_link": Venue.query.get_or_404(
                upcoming_show.venue_id).image_link,
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
        "seeking_venue": get_artist.seeking_venue,
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
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)

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
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)

    # TODO: populate form with values from venue with ID <venue_id> (DONE)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing (DONE)
    # venue record with ID <venue_id> using the new attributes

    error = False
    venue = Venue.query.get_or_404(venue_id)
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

    if form.validate_on_submit():
        try:
            new_artist = Artist()
            form.populate_obj(new_artist)

            db.session.add(new_artist)
            db.session.commit()

            flash('Artist ' + form.name.data + ' was successfully listed!')
        except():
            flash('Artist could not be listed :(')
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash(f"Errors: {message}")

    if not error:
        return render_template('pages/home.html')
    else:
        abort(500)
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. (DONE)
    # e.g.,
    # flash('An error occurred. Artist ' + data.name + ' could not be listed.')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    #       SQLAlchemy ORM to delete a record.
    #       Handle cases where the session commit could fail. (DONE)
    error = False

    try:
        artist_to_delete = Artist.query.get_or_404(artist_id)
        db.session.delete(artist_to_delete)
        db.session.commit()
        flash("Successfully deleted " + artist_to_delete.name + ".")
    except():
        db.session.rollback()
        flash(
            "Could not delete " + Artist.query.get_or_404(artist_id).name + ".")
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # TODO: BONUS CHALLENGE: Implement a button to delete a Venue on a
    #       Venue Page, have it so that clicking that button delete it
    #       from the db then redirect the user to the homepage (DONE)

    if not error:
        return redirect(url_for("index"))
    else:
        abort(500)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. num_shows should be aggregated
    #       based on number of upcoming shows per venue. (DONE)

    all_shows = Show.query.all()
    data = []

    for show in all_shows:
        data.append({
            "venue_id": Venue.query.get_or_404(show.venue_id).id,
            "venue_name": Venue.query.get_or_404(show.venue_id).name,
            "artist_id": Artist.query.get_or_404(show.artist_id).id,
            "artist_name": Artist.query.get_or_404(show.artist_id).name,
            "artist_image_link": Artist.query.get_or_404(
                show.artist_id).image_link,
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
    # called to create new shows in the db, upon submitting new show listing
    # form
    # TODO: insert form data as a new Show record in the db, instead (DONE)
    # on successful db insert, flash success

    error = False
    form = ShowForm(request.form)

    if form.validate_on_submit():
        try:
            req_venue_id = form.venue_id.data
            req_artist_id = form.artist_id.data
            req_start_time = form.start_time.data

            new_show = Show(venue_fk1=req_venue_id,
                            artist_fk2=req_artist_id,
                            start_time=req_start_time)

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
    else:
        flash("Show could not be created due to validation error!")

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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%('
            'lineno)d]')
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
