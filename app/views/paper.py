"""Paper Module
This module contains program code for displaying, adding, modifying,
and removing paper data.
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask import flash, abort
from app import db
from ..forms import PaperForm
from ..models import Paper, Inventory


paper = Blueprint("paper", __name__)

"""Returns the index dashboard for paper and displays the list of
papers, its dimension, and its no. of sheets available.
"""
@paper.route("/")
def index():
    papers = db.session.query(Paper, Inventory).join(Inventory).all()
    return render_template("paper/index.html", papers=papers)

"""Returns Add New Paper form.
This will add new paper to the database.
"""
@paper.route("/add", methods=["GET", "POST"])
def add():
    # Instantiates the form for adding new paper.
    form = PaperForm()
    # Checks whether the request method is GET or POST. Also checks if
    # the forms submitted are valid.
    if request.method == "POST" and form.validate():
        try:
            name = form.name.data
            dimension = form.dimension.data
            status = int(form.status.data)
            paper = Paper(
                name=name,
                dimension=dimension,
                status = status,
            )
            db.session.add(paper)
            # Saves the paper to the database.
            db.session.commit()
            # Get the newly added paper info from the database.
            paper = Paper.query.add_columns(Paper.id_paper)\
                    .order_by(Paper.id_paper.desc()).first()
            # Add the newly added paper to inventory table.
            inventory = Inventory(
                id_paper=paper.id_paper,
                no_pages=0
            )
            db.session.add(inventory)
            # Saves everything to the database.
            db.session.commit()
            flash(f"{name}({dimension}) Added Successfully!")
            return redirect(url_for("paper.index"))
        except:
            db.session.rollback()
            abort(500)
    else:
        # Returns add new paper page if the request method is GET or
        # one of the forms submitted contains invalid data.
        try:
            return render_template("paper/add.html", form=form)
        except:
            abort(500)

"""Returns Edit Paper form.
This will modify selected paper and update it to the database.
"""
@paper.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    try:
        # Instantiates the form for editing the paper information.
        form = PaperForm()
        # Checks whether the request method is GET or POST. Also checks
        # if the forms submitted are valid.
        if request.method == "POST" and form.validate():
            paper = Paper.query.get(id)
            paper.name = form.name.data
            paper.dimension = form.dimension.data
            paper.status = int(form.status.data)
            # Saves everything to the database.
            db.session.commit()
            flash("Updated Successfully!")
            return redirect(url_for("paper.index"))
        else:
            # Returns edit paper page if the request method is GET or
            # one of the forms submitted contains invalid data.
            paper = Paper.query.get(id)
            return render_template("paper/edit.html", form=form, paper=paper)
    except:
        db.session.rollback()
        flash("An error occured.")
        return redirect(url_for("paper.index"))

""" Delete selected paper.
This method will deleted the selected paper info from the database.
NOTE: Add new page for delete confirmation.
"""
@paper.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    try:
        if request.method == "POST":
            Paper.query.filter_by(id_paper=id).delete()
            db.session.commit()
            flash("Deleted Successfully!")
    except:
        db.session.rollback()
        abort(500)
    finally:
        return redirect(url_for("paper.index"))
