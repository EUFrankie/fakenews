from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import BasicUser


class BasicRegistration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=2, max=85)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = BasicUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken. Please choose a different one.')

    """
    def validate_email(self, email):
        user = Basic_User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in our system. Do you already have an account?')
    """


class DetailedRegistration(BasicRegistration):
    first_name = StringField('First name', validators=[DataRequired(),
                                                       Length(min=2, max=85)])
    middle_name = StringField('Middle name', validators=[Length(min=2, max=85)])
    last_name = StringField('Last name', validators=[DataRequired(),
                                                     Length(min=2, max=85)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = BasicUser.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Unknown username')


class ChangePassword(FlaskForm):
    password = PasswordField('Old password', validators=[DataRequired()])
    password_new = PasswordField('New password', validators=[DataRequired()])
    confirmation = PasswordField('Confirm password', validators=[DataRequired(),
                                                                 EqualTo('password_new')])
    submit = SubmitField("Change")