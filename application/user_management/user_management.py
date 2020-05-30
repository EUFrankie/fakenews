from flask import Blueprint, redirect, url_for, flash, render_template, request, session
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.user_management.user_forms import LoginForm, BasicRegistration, ChangePassword
from model import BasicUser
from application import db


user_bp = Blueprint("user_bp", __name__, template_folder="templates")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    # set the correct destination url after login
    if request.args.get("previous"):
        destination = request.args.get("previous")
        session["url"] = destination

    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('home_bp.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = BasicUser.query.filter_by(username=form.username.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if session["url"]:
                destination = session["url"]
                session.pop("url")
            else:
                destination = 'home_bp.home'
            # here we add the dynamic redirect
            return redirect(url_for(destination))
        else:
            flash("The login failed", "info")

    return render_template("login.html", form=form)


# for this route we actually need to be logged in already
# I need to figure out first how the redirecting stuff works with the login_required decorator
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user_bp.login", previous="user_bp.register"))

    form = BasicRegistration()

    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, salt_length=60)
        user = BasicUser(username=form.username.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home_bp.home'))

    return render_template("register.html", form=form)


@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home_bp.home"))


@user_bp.route("/password_reset", methods=["GET", "POST"])
@login_required
def password_reset():
    form = ChangePassword()

    if form.validate_on_submit():
        user = BasicUser.query.filter_by(username=current_user.username).first()
        user.password = generate_password_hash(form.password_new.data, salt_length=60)
        db.session.commit()

    return render_template("password_reset.html", form=form)


@user_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    render_template("settings.html")
