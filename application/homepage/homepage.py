from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home")
def home():
    team = ["dani", "elsa", "esther", "jan", "maurits", "myriam", "soutrik"]
    sources = {}
    for item in team:
        sources.update({item.capitalize(): f'team/{item}.png'})
    return render_template("landingpage.html", team=sources)


@home_bp.route("/testing")
def testing():
    return render_template("testhome.html")


@home_bp.route("/test")
def test():
    return render_template("landingpage_testing.html")


@home_bp.route("/testmau")
def testmau():
    return render_template("landingpage_testmau.html")


@home_bp.route("/api_documentation")
def api_doc():
    return render_template("api_doc.html")


@home_bp.route("/team")
def api_doc():
    return render_template("team.html")