from flask import Blueprint

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search")
def check_text():
    return "this worked"