"""Home Page
This module contains program code for calculating the printing sales
per transaction.
"""

from datetime import date
from flask import (
    Blueprint, render_template, jsonify, request, flash, abort
)
from app import db
from ..models import Paper, PrintCategory, PrintPrice, Sale, Inventory
from ..forms import IndexForm
import json
from sqlalchemy import text

home = Blueprint("home", __name__)

""" Returns the index page for print transaction page.
Also returns neccessary information to the user like how much the print
cost will be.
"""
@home.route("/home")
@home.route("/")
def index():
    try:

        # Get list of print categories in the database.
        categories = PrintCategory.query.filter_by(status=1).all()
        # Get list of papers in the database.
        papers = db.session.query(Paper, Inventory).join(Inventory).filter(
            Paper.status == 1,
            Inventory.no_pages > 0,
        ).all()
        # Extract id_category in categories object.
        id_category_list = [cat.id_category for cat in categories]
        # Get list of print_price.
        print_prices = PrintPrice.query.filter(
            PrintPrice.id_category.in_(id_category_list),
            PrintPrice.id_paper==1,
        ).all()
        # Instantiate form for Index Page.
        form = IndexForm()
        # Add list of papers as radiobutton.
        form.paper.choices = [
            (
                paper.id_paper,
                f"{paper.name} ({paper.dimension}) - {sheet.no_pages} sheets"
            )
            for paper, sheet in papers
        ]
        # Create new input field using the number of print_price.
        for _ in print_prices:
            form.categories.append_entry()

        # Rename the input field.
        for i in range(len(print_prices)):
            form.categories.entries[i].name = print_prices[i].id_print_price

        return render_template(
            "index.html",
            categories=categories,
            form=form,
        )
    except:
        abort(500)


@home.route("/testjson", methods=["GET", "POST"])
def json_this():
    amount_list = calculate()
    is_over = check_inventory()

    return jsonify(
        {
            'total_amount': sum(amount_list),
            'is_over': is_over,
        }
    )


@home.route("/savetransaction", methods=["GET", "POST"])
def save_transaction():
    try:
        is_over = check_inventory()
        amount_list = calculate()

        if is_over:
            # If is_over is True then no transaction will be saved.
            return jsonify(
                {
                    'total_amount': sum(amount_list),
                    'status': 'Fail',
                    'is_over': is_over,
                }
            )
        else:
            # If is_over is False then the transaction will be saved.
            print_prices = get_print_prices()
            sheets = json.loads(request.form["sheets"])
            paper_id = request.form["paper"]

            # Save to the database.
            for amount, price_id, sheet in zip(
                        amount_list,
                        [price_id.id_print_price for price_id in print_prices],
                        [sheet for sheet in sheets],
                                    ):
                if amount!=0:
                    sale = Sale(
                        id_print_price=price_id,
                        no_pages=sheet,
                        value=amount,
                        transaction_date=date.today()
                    )
                    db.session.add(sale)
                    # Subtract the printed sheets from the inventory.
                    inventory = Inventory.query.filter_by(
                                id_paper=text(f'{paper_id}')
                                ).first()
                    print(inventory)
                    inventory.no_pages = inventory.no_pages - int(sheet)
                    db.session.commit()
            
            flash('Saved Successfully!')
    except:
        db.session.rollback()
        flash('Unexpected Error')

    return jsonify(
        {
            'total_amount': sum(amount_list),
            'status': 'Success',
        }
    )


def calculate():
    # Get input values via Ajax in List format.
    input_dict = json.loads(request.form["sheets"])
    
    print_prices = get_print_prices()

    price_list = [price.price for price in print_prices]

    # Convert '' into 0.
    for i in range(len(input_dict)):
        if input_dict[i] == "":
            input_dict[i] = 0
    
    amount_list = []
    for price, sheet in zip(price_list, input_dict):
        price = float(price)
        sheet = float(sheet)
        amount_list.append(price*sheet)

    return amount_list


def get_print_prices():
    # Get list of print categories in the database.
    categories = PrintCategory.query.filter_by(status=1).all()
    # Extract id_category in categories object.
    id_category_list = [cat.id_category for cat in categories]
    paper = request.form["paper"]
    # Get the list of print prices from the database based on the list
    # of active categories and 
    print_prices = PrintPrice.query.filter(
        PrintPrice.id_category.in_(id_category_list)
    ).filter(PrintPrice.id_paper==text(f'{paper}')).all()

    return print_prices

# Check if the user's input of no. of sheets is more than the available
# sheets in the inventory.
def check_inventory():
    input_list = json.loads(request.form["sheets"])
    # Convert '' into 0.
    for i in range(len(input_list)):
        if input_list[i] == "":
            input_list[i] = 0
        else:
            input_list[i] = int(input_list[i])
    total_sheets = sum(input_list)
    paper = request.form["paper"]
    found_paper = Inventory.query.filter_by(id_paper=text(f'{paper}')).first()
    
    # Return True if the user inputted no. of sheets is greater than the 
    # available sheets in the inventory.
    if total_sheets > found_paper.no_pages:
        return True
    else:
        return False

