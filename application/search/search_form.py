from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchQueryForm(FlaskForm):
  query = StringField(label='Insert Claim', id="query", validators=[Length(min=1)])