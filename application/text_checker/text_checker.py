from flask import Blueprint, request
from application.text_checker.quick_solution_fuzzywuzzy import checker

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search1", methods=["GET", "POST"])
def check_text():
    if not request.form.get("user_input"):
        if not request.args.get("user_input"):
            return "input was false"
        else:
            text, score = checker(request.args.get("user_input"))
            return text + " with a score of " + str(score)
    else:
        text, score = checker(request.form.get("user_input"))
        return text + " with a score of " + str(score)


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
    print(user_input)
    if user_input:
        text, score = checker(user_input)
        print(text, score)
        return text + " with a score of " + str(score)
    return "didnt work"