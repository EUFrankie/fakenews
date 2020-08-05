from flask import Blueprint, request, jsonify, render_template, redirect, flash, url_for
import json
from model import Labels, Claims
from application import db
from flask_login import login_required, current_user
from sqlalchemy import desc, asc
import requests

label_bp = Blueprint("label_bp", __name__, template_folder="templates")


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
def label():
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user_bp.login", previous="label_bp.label"))

    claim_ids = [11, 18, 19, 25, 30]
    checked_claims = ["checking1", "smoething else1", "also checking1", "hahahaha1", "kaodejisdjiofjds1"]
    labels = [0, 1, 0, 1, 0]

    for i in range(len(claim_ids)):
        label = Labels(original_id=claim_ids[i],
                       check_claim=checked_claims[i],
                       label=labels[i])
        db.session.add(label)

    db.session.commit()

    # we get the top 20 lowest labelled items
    claim = Claims.query.order_by(desc(Claims.id)).limit(10).all()

    return render_template("labeltool.html", claim=claim)


@label_bp.route("/metrics", methods=["GET", "POST"])
def metrics():
    # this is not a priority
    return "to do"


def get_claims():
    """
    https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search
    """

    API_key = "AIzaSyCrvjCI5k6XGP9tn9sos29PTNgOFnt7_G4"

    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    param = {
        "query": "testing",
        "key": API_key,
        "languageCode": "en",
        "pageSize": 20,
        "reviewPublisherSiteFilter": None
    }

    results = requests.get(url=url, params=param)

    return results


def get_google_searches(search: str):
    """
    https://developers.google.com/custom-search/v1/using_rest
    """

    API_key = "AIzaSyCrvjCI5k6XGP9tn9sos29PTNgOFnt7_G4"
    url = "https://www.googleapis.com/customsearch/v1"
    google = "005366740491259083467:rbgacuprvi7"
    search = search

    param = {
        "q": search,
        "key": API_key,
        "cx": google
    }

    results = request.get(url=url, params=param)

    return results
