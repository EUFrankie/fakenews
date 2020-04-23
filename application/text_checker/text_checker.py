from flask import Blueprint

text_bp = Blueprint("text_bp", __name__)


@text_bp.route("/")
def check_text():
    pass

