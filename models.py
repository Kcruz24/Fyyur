# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String
#
# app = Flask(__name__)
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)
#
#
# # ----------------------------------------------------------------------------#
# # Models.
# # ----------------------------------------------------------------------------#
# class Show(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     venue_fk1 = db.Column(db.Integer(), db.ForeignKey('venue.id'), nullable=False)
#     artist_fk2 = db.Column(db.Integer(), db.ForeignKey('artist.id'), nullable=False)
#     start_time = db.Column(db.DateTime(), nullable=False)
#
#     def __repr__(self):
#         return f"id: {self.id}, venue_fk: {self.venue_fk1}, artist_fk: {self.artist_fk2}, start_time: {self.start_time}"
#
#
# class Venue(db.Model):
#     __tablename__ = 'venue'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     address = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=False)
#     genres = db.Column(db.ARRAY(String), nullable=False)
#     facebook_link = db.Column(db.String(120), nullable=True)
#     image_link = db.Column(db.String(500), nullable=False)
#     website_link = db.Column(db.String(500), nullable=False)
#     seeking_talent = db.Column(db.Boolean(), nullable=True, default=False)
#     seeking_description = db.Column(db.String(), nullable=True)
#     shows = db.relationship('Show', backref='venue', lazy='joined', cascade='all, delete')
#
#     def __repr__(self):
#         return f"Table id: {self.id}, name: {self.name}"
#
#
# class Artist(db.Model):
#     __tablename__ = 'artist'
#
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=False)
#     genres = db.Column(db.ARRAY(String), nullable=False)
#     facebook_link = db.Column(db.String(120), nullable=True)
#     image_link = db.Column(db.String(500), nullable=False)
#     website_link = db.Column(db.String(500), nullable=True)
#     seeking_venues = db.Column(db.Boolean(), nullable=True, default=False)
#     seeking_description = db.Column(db.String(), nullable=True)
#     shows = db.relationship('Show', backref='artist', lazy='joined', cascade='all, delete')
#
#     def __repr__(self):
#         return f"id: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, " \
#                f"phone: {self.phone}, genres: {self.genres}, facebook_link: {self.facebook_link}, " \
#                f"image_link: {self.image_link}, website_link: {self.website_link}, seeking_venues: {self.seeking_venues}, " \
#                f"seeking_description: {self.seeking_description}"