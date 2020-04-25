from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home")
def home():
    return render_template("landingpage.html")


@home_bp.route("/testing")
def testing():
    return render_template("testhome.html")


@home_bp.route("/test")
def test():
    return render_template("landingpage_testing.html")