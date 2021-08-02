from flask import Blueprint, render_template

error_handlers = Blueprint("error_handlers", __name__)


@error_handlers.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@error_handlers.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
