from flask import Blueprint, request
from application.text_checker.quick_solution_fuzzywuzzy import basic_checker, checker

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search1", methods=["GET", "POST"])
def check_text():
    if not request.form.get("user_input"):
        if not request.args.get("user_input"):
            return "input was false"
        else:
            response = checker(request.args.get("user_input"))
            return response
    else:
        response = checker(request.form.get("user_input"))
        return response


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
    if user_input:
        response = checker(user_input)
        return response
    return "didnt work"