from flask import Blueprint, render_template
from app import db
from ..models import Paper

home = Blueprint("home", __name__)

@home.route("/home")
@home.route("/")
def index():
    return render_template("index.html")

