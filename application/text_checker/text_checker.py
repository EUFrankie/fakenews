from flask import Blueprint, request, jsonify
from application.text_checker.quick_solution_fuzzywuzzy import basic_checker, checker

text_bp = Blueprint("text_bp", __name__, template_folder="templates")


@text_bp.route("/search1", methods=["GET", "POST"])
def check_text():
    print("is this executed?")
    if not request.form.get("user_input"):
        if not request.args.get("user_input"):
            return "input was false"
        else:
            input = request.args.get("user_input")
            if isinstance(input, list):
                output = []
                for item in input:
                    output.append(checker(item))
                return jsonify({"output": output})
            elif isinstance(input, str):
                print("we got to the str part")
                output = checker(input)
                print({"output": output})
                return jsonify({"output": output})
            else:
                return jsonify({"output": None})
    else:
        response = checker(request.form.get("user_input"))
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

        return "it is not none" \
               "with sentences {}" \
               "and output {}".format(sentences, output)

    return "didnt work"