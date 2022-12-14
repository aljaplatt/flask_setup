from app import app
from book_routes.routes import book_req
# change to reservations.reservations
from reservation_routes.routes import reservation_req


 # Register Blueprints - tell our Flask app that this blueprint and its routes exist
app.register_blueprint(book_req, url_prefix="/books")
# put reservations.py in its own reservations folder
app.register_blueprint(reservation_req, url_prefix="/books")

# book_req and reservation_req are the names of our blueprints. These are imported above from the books module.

# url_prefix is optional - but this allows you to state it here and not have to type on each route. You prefix every route in this blueprint with /books.

