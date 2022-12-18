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
from ..models import PrintPrice

price = Blueprint("price", __name__)

"""Returns the index dashboard for print prices and displays the
list of print prices and its values.
"""
@price.route("/")
def index():
    return render_template("price/index.html")