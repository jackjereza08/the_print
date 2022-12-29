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
from ..forms import PriceForm
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