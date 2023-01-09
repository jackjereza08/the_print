"""Price Module
This module contains program code for displaying, adding, modifying,
and removing printing price.

The price module will set the price standard for printing documents
based on their print category, the printing type (BW or COLORED), and
the type of paper to use.
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask import flash, abort
from app import db
from ..models import PrintPrice, PrintCategory, Paper

price = Blueprint("price", __name__)

"""Returns the index dashboard for print prices and displays the
list of print prices and its values.
"""
@price.route("/")
def index():
    header = display_header()
    data = display_data()
    return render_template("price/index.html", header=header, data=data)


@price.route("/edit-prices", methods=["GET","POST"])
def edit():
    # Gets data from the database for display.
    header = display_header()
    data = display_data()
    # Instantiates the form for editing print prices.
    # form = PriceForm()
    # Checks whether the request method is GET or POST. Also checks if
    # the forms submitted are valid.
    try:
        if request.method == "POST":
            for i in range(len(data)):
                id = i+1
                updated_price = PrintPrice.query.get(id)
                updated_price.price = request.form[f"{id}"]
                db.session.commit()

            flash("Updated Successfully!")
            return redirect(url_for("price.index"))
        else:
            return render_template(
                "price/edit.html",
                header=header,
                data=data,
                # form=form,
            )
    except:
        db.session.rollback()
        flash("An error occured.")
        return redirect(url_for("price.index"))

# Display Category header at Print Price page.
def display_header():
    category = PrintCategory.query.all()
    return category

# Display price data at Print Price page.
def display_data():
    price = db.session.query(
        PrintPrice,
        PrintCategory,
        Paper,
    ).join(
        PrintCategory,
        Paper,
    ).order_by(
        PrintPrice.id_paper
    ).all()
    
    return price