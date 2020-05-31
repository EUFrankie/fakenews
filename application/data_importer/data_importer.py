from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from .dataforms import DataUpload, create_match_form
from flask_login import current_user
import pandas as pd
from application import db
from model import Claims
import json
import datetime

data_in_bp = Blueprint("data_in_bp", __name__,
                       template_folder="templates", static_folder="static")


@data_in_bp.route("/data", methods=["GET", "POST"])
def data():
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user_bp.login", previous="data_in_bp.data"))

    form = DataUpload()

    if form.validate_on_submit():
        # we read in the file
        file_name = form.file_name.data.filename
        data = request.files.get("file_name")
        if file_name.endswith(".csv"):
            uploaded_data = pd.read_csv(data)

        elif file_name.endswith(".xlsx"):
            uploaded_data = pd.read_excel(data)
        else:
            flash("Something was wrong with the uploaded file")
            return redirect(url_for("data_in_bp.data"))

        # we get column names of both uploaded file and db
        file_columns = uploaded_data.columns.values
        db_columns = Claims.__table__.columns.keys()
        exclude = ["id", "added_by", "date_added_to_db"]
        for item in exclude:
            db_columns.remove(item)

        # we try the first matching
        matches = {}
        for item in db_columns:
            for file_item in file_columns:
                if item == file_item:
                    matches.update({item: file_item})
                    break

        if not len(matches) == len(db_columns):
            # we store in the session variable to make it accessible across routes
            # not sure if this is the best method to do so
            session["db_columns"] = db_columns
            session["file_columns"] = file_columns.tolist()
            session["location"] = "application"+url_for("data_in_bp.static", filename="temp_files/"+file_name)

            # we store the data in temp csv file
            if file_name.endswith(".csv"):
                uploaded_data.to_csv(session.get("location"))
            elif file_name.endswith(".xlsx"):
                uploaded_data.to_excel(session.get("location"))
            else:
                flash("Something was wrong with the uploaded file")
                return redirect(url_for("data_in_bp.data"))
            return redirect(url_for("data_in_bp.matching"))

        else:
            # here we wanna simply add the data to db
            add_to_db(uploaded_data, matches)
            return redirect(url_for("home_bp.home"))

    return render_template("data.html", form=form)


def add_to_db(datafile, matches):
    if not isinstance(datafile, pd.DataFrame) or not isinstance(matches, dict):
        flash("Something went wrong")
        return redirect("home_bp.home")
    else:
        # we make sure we can upload the dataframe
        to_upload = pd.DataFrame()
        for item in matches:
            to_upload[item] = datafile[matches[item]]
        to_upload["date_added_to_db"] = datetime.datetime.utcnow()
        to_upload["added_by"] = current_user.id

        flash("The upload was successful")
        con = db.engine
        to_upload.to_sql(name="claims", con=con, if_exists="append", index=False)


@data_in_bp.route("/matching", methods=["GET", "POST"])
def matching():
    # we create the matching form
    form = create_match_form(match_data=session.get("db_columns"), choices=session.get("file_columns"))

    if form.validate_on_submit():
        matches = {}
        for field in form:
            if field.name != "submit" and field.name != "csrf_token" and field.data != "irrelevant":
                matches.update({field.name: field.data})

        if session.get("location").endswith(".csv"):
            datafile = pd.read_csv(session.get("location"))
        elif session.get("location").endswith(".xlsx"):
            datafile = pd.read_excel(session.get("location"))
        else:
            flash("Something went wrong in the backend, you've been redirected to the homepage")
            return redirect(url_for("home_bp.home"))

        add_to_db(datafile, matches)
        return redirect(url_for("home_bp.home"))

    return render_template("matches.html", form=form)