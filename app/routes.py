from . import app
from .views.home import home
from .views.paper import paper
from .views.inventory import inventory
from .views.category import category
from .views.price import price

# Register the blueprints here.
app.register_blueprint(home)
app.register_blueprint(paper, url_prefix="/dashboard/paper")
app.register_blueprint(inventory, url_prefix="/dashboard/inventory")
app.register_blueprint(category, url_prefix="/dashboard/category")
app.register_blueprint(price, url_prefix="/dashboard/price")