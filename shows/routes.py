import sys
from flask import flash, render_template, abort, request, Blueprint
from shows.forms import ShowForm
from models import Show, db, Artist, Venue

shows = Blueprint("shows", __name__)


#  Shows
#  ----------------------------------------------------------------
@shows.route('/shows')
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


@shows.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@shows.route('/shows/create', methods=['POST'])
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
