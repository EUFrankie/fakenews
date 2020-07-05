from flask import Blueprint, request, jsonify
from application.text_checker.text_matcher import best_matches, one_best_match, list_matches
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
          output.append(best_matches(item))
        return jsonify({"output": output})
      elif isinstance(input, str):
        output = best_matches(input)
        return jsonify({"output": output})
      else:
        return jsonify({"output": None})
  else:
    response = best_matches(request.form.get("user_input"))
    return response


@text_bp.route("/search2/<user_input>", methods=["GET", "POST"])
def check_text2(user_input):
  if user_input:
    response = one_best_match(user_input)
    return response
  return "didnt work"


@text_bp.route("/best_match", methods=["GET", "POST"])
def check_text3():
  if request.get_json():
    input = request.get_json()
    if "queries" not in input:
      return jsonify({"error": "The request must contain the field 'queries'."})

    if not isinstance(input['queries'], list):
      return jsonify({"error": "Queries must be a list."})

    queries = input["queries"]

    output = []
    for item in queries:
      output.append(one_best_match(item))

    return jsonify(output)
  else:
    return jsonify({"error": "The request must contain a json body and Content-Type application/json must be set."})

@text_bp.route("/list_matching", methods=["POST"])
def list_matching_view():
  if request.get_json():
    if "queries" in request.json and "corpus" in request.json:
      if not isinstance(request.json['queries'], list):
        return jsonify({"error": "Queries must be a list."})
      if not isinstance(request.json['corpus'], list):
        return jsonify({"error": "Corpus must be a list."})
      return jsonify(list_matches(request.json['queries'], request.json['corpus']))
    else:
      return jsonify({"error": "The request must contain the fields 'queries' and 'corpus'."})
  else:
    return jsonify({"error": "The request must contain a json body and Content-Type application/json must be set."})