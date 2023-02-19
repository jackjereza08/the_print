"""Printing Category Module
This module contains program code for displaying, adding, modifying,
and removing paper printing category.

Printing Category is based on print type, ink usage, and paper type. It
is used to standardize printing price.

E.g. category 'TextPrint' is for printing documents containing text 
only.

A category (e.g.'TextPrint') will have a different price for
Black/White and Colored printing. It means that there will be two the
same category and two different price for PrintPrice model.

E.g. In 'PrintPrice' model: 'TextPrint(BW)' and TextPrint(COLORED).
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask import flash, abort
from app import db
from ..forms import CategoryForm
from ..models import PrintCategory, Paper, PrintPrice

category = Blueprint("category", __name__)

"""Returns the index dashboard for print categories and displays the
list of print categories and its status.
"""
@category.route("/")
def index():
    print_categories = PrintCategory.query.all()
    # Return if there is a paper in the database else the user should
    # add paper first before adding print category.
    paper_count = Paper.query.count()
    return render_template(
        "category/index.html",
        print_categories=print_categories,
        paper_count=paper_count,
    )

"""Returns Add New Category form.
This will add new print category to the database.
"""
@category.route("/add-category", methods=["GET", "POST"])
def add():
    # Instantiates the form for adding new category.
    form = CategoryForm()
    # Checks whether the request method is GET or POST. Also checks if
    # the forms submitted are valid.
    if request.method == "POST" and form.validate():
        try:
            category_name = form.category_name.data
            # Status will change its type from Boolean to Integer since
            # the status column accepts Integers only.
            status = int(form.status.data)
            print_category = PrintCategory(
                category_name=category_name,
                status=status
            )
            db.session.add(print_category)
            # Saves everything to the database.
            db.session.commit()
            # Add automatic to the database the paper-category-price
            # relationship(print_price).
            # NOTE: This is experimental.
            category = PrintCategory.query.add_columns(
                PrintCategory.id_category
            ).order_by(
                PrintCategory.id_category.desc()
            ).first()
            
            configure_price_db()

            flash(f"{category_name} Added Successfully!")
            return redirect(url_for("category.index"))
        except:
            db.session.rollback()
            abort(500)
    else:
        # Return if there is a paper in the database else the user should
        # add paper first before adding print category.
        paper_count = Paper.query.count()
        if paper_count > 0:
            # Returns add new category if the request method is GET or
            # one of the forms submitted contains invalid data.
            return render_template("category/add.html", form=form)
        else:
            flash("Add paper in the database first.")
            return redirect(url_for('paper.index'))

"""Returns Edit Paper form.
This will modify selected paper and update it to the database.
"""
@category.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    try:
        # Instantiates the form for editing the category information.
        form = CategoryForm()
        # Checks whether the request method is GET or POST. Also checks
        # if the forms submitted are valid.
        if request.method == "POST" and form.validate():
            category = PrintCategory.query.get(id)
            category.category_name = form.category_name.data
            # Status will change its type from Boolean to Integer since
            # the status column accepts Integers only.
            category.status = int(form.status.data)
            # Saves everything to the database.
            db.session.commit()
            configure_price_db()
            flash("Updated Successfully!")
            return redirect(url_for("category.index"))
        else:
            # Returns edit paper page if the request method is GET or
            # one of the forms submitted contains invalid data.
            category = PrintCategory.query.get(id)
            return render_template(
                "category/edit.html",
                form=form,
                category=category
            )
    except Exception as e:
        db.session.rollback()
        flash("An error occured.")
        return redirect(url_for("category.index"))


def configure_price_db():
    papers = Paper.query.all()
    categories = PrintCategory.query.all()

    for paper in papers:
        for category in categories:
            # Checks if category and paper are already in print_price.
            count = PrintPrice.query.filter(
                PrintPrice.id_paper == paper.id_paper,
                PrintPrice.id_category == category.id_category
            ).count()

            if count > 0:
                # If found then continue to the next category.
                continue
            else:
                # If not found then perform insertion of Print Price
                # to the print_price table.

                # Black/White print type.
                db.session.add(
                    PrintPrice(
                            id_paper=paper.id_paper,
                            id_category=category.id_category,
                            print_type="BLK",
                            price=0.00
                        )
                )
                # Colored print type.
                db.session.add(
                    PrintPrice(
                            id_paper=paper.id_paper,
                            id_category=category.id_category,
                            print_type="CLR",
                            price=0.00
                        )
                )
    # Saves everything to the database.
    db.session.commit()
