from flask import Blueprint, request
from application.text_checker.quick_solution_fuzzywuzzy import checker

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search1", methods=["GET", "POST"])
def check_text():
    input = request.form.get("input")
    print(input)
    if input:
        text, score = checker(input)
        print(text, score)
        return text + " with a score of " + str(score)
    return "didnt work"


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
    print(user_input)
    if user_input:
        text, score = checker(user_input)
        print(text, score)
        return text + " with a score of " + str(score)
    return "didnt work"


@text_bp.route("/search3", methods=["GET", "POST"])
def check_text3():
    user_input = request.args.get("input")
    print(user_input)
    if user_input:
        text, score = checker(user_input)
        print(text, score)
        return text + " with a score of " + str(score)
    return "didnt work"