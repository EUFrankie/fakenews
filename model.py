from flask_login import UserMixin
from sqlalchemy.sql import func, text
from sqlalchemy import event
from application import db, login_manager


# this takes care of all user sessions together with the Usermixin class
@login_manager.user_loader
def load_user(id):
    return BasicUser.query.get(int(id))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    check_claim = db.Column(db.String, nullable=False)
    feedback_label = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DATETIME(timezone=True), server_default=func.now(), nullable=False)


# label class
class Labels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    check_claim = db.Column(db.String, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DATETIME(timezone=True), server_default=func.now(), nullable=False)


# the data that we check against
class Claims(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    explanation = db.Column(db.String)
    fact_checker = db.Column(db.String)
    url_checker = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.DATE)
    label = db.Column(db.String)
    claim_originated_by = db.Column(db.String)
    date_added_to_db = db.Column(db.DATETIME(timezone=True), server_default=func.now())
    added_by = db.Column(db.Integer, db.ForeignKey("basic_user.id"))
    label_count = db.Column(db.Integer, server_default=text("0"))
    feedback_count = db.Column(db.Integer, server_default=text("0"))

    original = db.relationship('Labels', backref='original', lazy=True)
    feedback = db.relationship("Feedback", backref='original', lazy=True)

    @event.listens_for(Labels, "after_insert")
    def label_count_increase(mapper, connection, label):
        Claims.query.filter_by(id=int(label.original_id)).update({Claims.label_count: Claims.label_count + 1})

    @event.listens_for(Feedback, "after_insert")
    def feedback_count_increase(mapper, connection, feedback):
        Feedback.query.filter_by(id=int(feedback.original_id)).update({Claims.feedback_count: Claims.feedback_count + 1})

    def __repr__(self):
        return "{id: " + str(self.id)+" claim: " + self.title + " label_count: " + str(self.label_count)+"}"


# the user
class BasicUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    claims = db.relationship("Claims", backref="user", lazy=True)
