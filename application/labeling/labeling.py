from flask import Blueprint, request, jsonify, render_template
import json
from model import Labels
from application import db
from flask_login import login_required

label_bp = Blueprint("label_bp", __name__)


@label_bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.get_json():
        db_input = request.get_json()
        label = Labels(original=db_input["claim"],
                       check_claim=db_input["search"],
                       label=db_input["label"])
        db.session.add(label)
        try:
            db.session.commit()
        except:
            return jsonify({"response": False})
        return jsonify({"response": True})
    return jsonify({"response": False})


@label_bp.route("/label")
@login_required
def label():
    # we get the top 20 lowest labelled items
    return render_template("labeltool.html")


@label_bp.route("/metrics", methods=["GET", "POST"])
def metrics():
    # this is not a priority
    return "to do"

