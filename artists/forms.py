from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SelectField,
                     SelectMultipleField,
                     BooleanField)
from wtforms.validators import DataRequired, URL, Regexp, Optional

from enums import Genre, State


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for phone (DONE)
        'phone', validators=[
            Regexp(r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
        ]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )

    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
        'seeking_description'
    )
