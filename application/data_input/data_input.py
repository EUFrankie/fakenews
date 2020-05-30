from flask import Blueprint, render_template, flash, redirect, url_for, request
from .dataforms import DataUpload
from flask_login import current_user
import pandas as pd
from application import db

data_in_bp = Blueprint("data_in_bp", __name__, template_folder="templates")


@data_in_bp.route("/data", methods=["GET", "POST"])
def data():
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user_bp.login", previous="data_in_bp.data"))

    form = DataUpload()

    if form.validate_on_submit():
        file_name = form.file_name.data.filename
        data = request.files.get("file_name")
        if file_name.endswith(".csv"):
            uploaded_data = pd.read_csv(data)
        elif file_name.endswith(".xlsx"):
            uploaded_data = pd.read_excel(data)
        else:
            flash("Something was wrong with the uploaded file")
            return redirect(url_for("data_in_bp.data"))

        i = 0
        for index, row in uploaded_data.iterrows():
            if i > 5:
                break
            else:
                print("index", index, "row", row["date"], "i", i)
                i += 1

    return render_template("data.html", form=form)