from flask import Blueprint, request, jsonify
from application.text_checker.quick_solution_fuzzywuzzy import basic_checker, checker, checker_options
import json

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search1", methods=["GET", "POST"])
def check_text():
    if not request.form.get("user_input"):
        if not request.args.get("user_input"):
            return jsonify({"output": None})
        else:
            input = request.args.get("user_input")
            if isinstance(input, list):
                output = []
                for item in input:
                    output.append(checker_options(item))
                return jsonify({"output": output})
            elif isinstance(input, str):
                output = checker_options(input)
                return jsonify({"output": output})
            else:
                return jsonify({"output": None})
    else:
        response = checker_options(request.form.get("user_input"))
        return response


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
    if user_input:
        response = checker(user_input)
        return response
    return "didnt work"


@text_bp.route("/search_json", methods=["GET", "POST"])
def check_text3():
    if request.get_json():
        input = request.get_json()
        sentences = input["sentences"]

        output = []
        for item in sentences:
            output.append(checker(item))

        return jsonify(output)

    return "didnt work"