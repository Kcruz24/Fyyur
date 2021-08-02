import sys
from datetime import datetime
from flask import (render_template,
                   flash,
                   abort,
                   request,
                   redirect,
                   url_for,
                   Blueprint)

from artists.forms import ArtistForm
from models import Artist, db, Venue
from venues.forms import VenueForm

artists = Blueprint("artists", __name__)


#  Artists
#  ----------------------------------------------------------------
@artists.route('/artists')
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


@artists.route('/artists/search', methods=['POST'])
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


@artists.route('/artists/<int:artist_id>')
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
@artists.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id> (DONE)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artists.route('/artists/<int:artist_id>/edit', methods=['POST'])
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


@artists.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)

    # TODO: populate form with values from venue with ID <venue_id> (DONE)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@artists.route('/venues/<int:venue_id>/edit', methods=['POST'])
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
        return redirect(url_for('venues.show_venue', venue_id=venue_id))
    else:
        abort(500)


#  Create Artist
#  ----------------------------------------------------------------

@artists.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@artists.route('/artists/create', methods=['POST'])
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


@artists.route('/artists/<artist_id>/delete', methods=['DELETE'])
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
        return redirect(url_for("main.index"))
    else:
        abort(500)
