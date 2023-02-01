""" This is the model needed to create database for this app. To create
database, go to __init__ file of the app and add 'from . import models'
without the quote inside 'with app.app_context():' then run the app.
    If importation of models is already in app context, leave it there.
"""
from . import db

# Collection of Papers
class Paper(db.Model):
    __tablename__ = "papers"
    id_paper = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    dimension = db.Column(db.String(100))

    def __init__(self, name, dimension):
        self.name = name
        self.dimension = dimension

# Collection of Sales
class Sale(db.Model):
    __tablename__ = "sales"
    id_sales = db.Column(db.Integer, primary_key = True)
    id_print_price = db.Column(
        db.Integer,
        db.ForeignKey('print_prices.id_print_price')
    )
    no_pages = db.Column(db.Integer)
    value = db.Column(db.Float)
    transaction_date = db.Column(db.Text)

    def __init__(self, id_print_price, no_pages, value,
     transaction_date):
        self.id_print_price = id_print_price
        self.no_pages = no_pages
        self.value = value
        self.transaction_date = transaction_date

# Collection of Price cost based on type of printing.
class PrintPrice(db.Model):
    __tablename__ = "print_prices"
    id_print_price = db.Column(db.Integer, primary_key = True)
    id_category = db.Column(
        db.Integer,
        db.ForeignKey('print_categories.id_category')
        )
    id_paper = db.Column(db.Integer, db.ForeignKey('papers.id_paper'))
    print_type = db.Column(db.String(5))
    price = db.Column(db.Float)

    def __init__(self, id_category, id_paper, print_type, price):
        self.id_category = id_category
        self.id_paper = id_paper
        self.print_type = print_type
        self.price = price

# Collection of category based on print type, ink usage, and paper.
class PrintCategory(db.Model):
    __tablename__ = "print_categories"
    id_category = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(5))
    status = db.Column(db.Integer)

    def __init__(self, category_name, status):
        self.category_name = category_name
        self.status = status

# Collection of Paper inventory.
class Inventory(db.Model):
    __tablename__ = "inventories"
    id_inventory = db.Column(db.Integer, primary_key = True)
    id_paper = db.Column(db.Integer, db.ForeignKey('papers.id_paper'))
    no_pages = db.Column(db.Integer)

    def __init__(self, id_paper, no_pages):
        self.id_paper = id_paper
        self.no_pages = no_pages

# Collection of cost of paper purchased and number of sheets.
class Cost(db.Model):
    __tablename__ = "costs"
    id_cost = db.Column(db.Integer, primary_key = True)
    id_paper = db.Column(db.Integer, db.ForeignKey('papers.id_paper'))
    no_pages = db.Column(db.Integer)
    purchase_cost = db.Column(db.Float)
    purchase_date = db.Column(db.Text)

    def __init__(self, id_paper, no_pages, purchase_cost, purchase_date):
        self.id_paper = id_paper
        self.no_pages = no_pages
        self.purchase_cost = purchase_cost
        self.purchase_date = purchase_date
        