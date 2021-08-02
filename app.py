# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask

from venues.routes import venues
from artists.routes import artists
from shows.routes import shows
from main.routes import main
from error_handlers.routes import error_handlers

app = Flask(__name__)


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
# Routes.
# ----------------------------------------------------------------------------#
app.register_blueprint(main)
app.register_blueprint(venues)
app.register_blueprint(artists)
app.register_blueprint(shows)
app.register_blueprint(error_handlers)

# ----------------------------------------------------------------------------#
# Error log.
# ----------------------------------------------------------------------------#
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
