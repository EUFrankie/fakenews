from flask import Blueprint, request, jsonify
from application.text_checker.text_matcher import find_best_matches, find_one_best_match
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
                    output.append(find_best_matches(item))
                return jsonify({"output": output})
            elif isinstance(input, str):
                output = find_best_matches(input)
                return jsonify({"output": output})
            else:
                return jsonify({"output": None})
    else:
        response = find_best_matches(request.form.get("user_input"))
        return response


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
    if user_input:
        response = find_one_best_match(user_input)
        return response
    return "didnt work"


@text_bp.route("/search_json", methods=["GET", "POST"])
def check_text3():
    if request.get_json():
        input = request.get_json()
        sentences = input["sentences"]

        output = []
        for item in sentences:
            output.append(find_one_best_match(item))

        return jsonify(output)

    return "didnt work"