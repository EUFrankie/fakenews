from application import db, login_manager
import datetime
import pytz
from flask_login import UserMixin
from sqlalchemy.sql import func


# this takes care of all user sessions together with the Usermixin class
@login_manager.user_loader
def load_user(id):
    return BasicUser.query.get(int(id))


# label class
class Labels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    check_claim = db.Column(db.String, nullable=False)
    feedback_label = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DATETIME(timezone=True), server_default=func.now(), nullable=False)


# the data that we check against
class Claims(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    explanation = db.Column(db.String, nullable=False)
    fact_checker = db.Column(db.String)
    url_checker = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.DATETIME)
    label = db.Column(db.String, nullable=False)
    claim_originated_by = db.Column(db.String)
    date_added_to_db = db.Column(db.DATETIME(timezone=True), server_default=func.now(), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey("basic_user.id"), nullable=False)

    original = db.relationship('Labels', backref='original', lazy=True)


# the user
class BasicUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    claims = db.relationship("Claims", backref="user", lazy=True)
