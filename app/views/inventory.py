"""Inventory Module
This module contains program code for displaying and adding inventory
of a certain paper.
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask import flash, abort
from app import db
from ..forms import PurchaseForm
from ..models import Inventory, Paper, Cost


inventory = Blueprint("inventory", __name__)

"""Returns the index dashboard for inventory and displays the list of
papers and its no of sheets available.
"""
@inventory.route("/")
def index():
    try:
        inventory_list = db.session.query(Inventory, Paper).join(Paper).all()
        return render_template(
            "inventory/index.html",
            inventory_list=inventory_list
            )
    except:
        abort(500)

"""Returns purhcase form.
This will add purchase cost and inventory to the database.
"""
@inventory.route("/add-purchase/<id>", methods=["GET", "POST"])
def add(id):
    # Gets the current paper data from the database.
    paper = Paper.query.get(id)
    # Instantiates the form for adding purchased paper.
    form = PurchaseForm()
    # Checks whether the request method is GET or POST. Also checks if
    # the forms submitted are valid.
    if request.method == "POST" and form.validate():
        try:
            paper_cost = Cost(
                id_paper=id,
                no_pages=form.no_pages.data,
                purchase_cost=form.purchase_cost.data,
                purchase_date=form.purchase_date.data
            )
            db.session.add(paper_cost)
            # Finds the paper via its id and change the no. of sheets
            # by adding the no of sheets purchased.
            found_paper = Inventory.query.filter_by(id_paper=id).first()
            found_paper.no_pages = found_paper.no_pages + form.no_pages.data
            # Saves everything to the database.
            db.session.commit()
            flash("Saved Successfully!")
            return redirect(url_for("paper.index"))
        except:
            db.session.rollback()
            abort(500)
    else:
        # Returns add purchase page if the request method is GET or
        # one of the forms submitted contains invalid data.
        try:
            return render_template(
                "inventory/add_purchase.html",
                form=form,
                paper=paper
                )
        except:
            abort(500)