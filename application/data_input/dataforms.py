from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class DataUpload(FlaskForm):
    file_name = FileField("File upload", validators=[DataRequired()])
    submit = SubmitField("Upload")