from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField, SelectField
from wtforms.validators import DataRequired


class DataUpload(FlaskForm):
    file_name = FileField("File upload", validators=[DataRequired(),
                                                     FileAllowed(["csv", "xlsx"],
                                                                 "only csv and xslx files are allowed")])
    submit = SubmitField("Upload")


def create_match_form(match_data, choices):
    class MatchData(FlaskForm):
        submit = SubmitField("confirm")

    choices_reworked = [(0, "irrelevant")]
    for item in choices:
        choices_reworked.append((item, item))

    for item in match_data:
        setattr(MatchData, item, SelectField(item, validators=[DataRequired()], choices=choices_reworked))

    form = MatchData()

    return form