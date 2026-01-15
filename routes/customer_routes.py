from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc, or_
from database import db
from models.model import Customer

# url prefix means that all routes get /customer before them in the browser
customer_bp = Blueprint("customer", __name__, url_prefix="/customer")


# länken blir customer.get_all
# namespace är alltså customer, eftersom det är den som står först i Blueprint
@customer_bp.route("/")
def get_all():
    # This is our base query. Note that there is no .all() or .first() at the end
    # We want this to be a Query object
    query = db.session.query(Customer)

    # These are possible query parameters that we get from the URL
    # the pattern for query params is:
    # ? this starts the request
    # parameter_name=value
    # & this is used to get multiple values
    # /?page=10&per_page=20 means that the page is 10 and we have 20 per_page
    q = request.args.get("q", default="", type=str)
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=50)
    sort_order = request.args.get("sort_order", type=str, default="asc")
    sort_by = request.args.get("sort_by", type=str, default="Id")

    # 50 because the task says 50 in the text.
    # Magic number
    max_per_page = 50

    # If we get a value from the search bar, called q, we search using ilike
    # ilike = case-insensitive search. We use % % around q to make it a wildcard search
    if q:
        query = query.where(
            or_(
                Customer.City.ilike(f"%{q}%"),
                Customer.GivenName.ilike(f"%{q}%"),
                Customer.Surname.ilike(f"%{q}%"),
            )
        )

    # We assume Customer.Id is standard sorting since it usually is the default
    sorting = Customer.Id

    # if we have sort_by params in the query string that match, we change it.
    if sort_by == "Name":
        sorting = Customer.GivenName
    elif sort_by == "Address":
        sorting = Customer.Streetaddress

    # At the end we add the sorting order.
    # Descending or ascending?
    if sort_order == "asc":
        query = query.order_by(asc(sorting))
    elif sort_order == "desc":
        query = query.order_by(desc(sorting))

    # db.paginate wants the new SQLAlchemy select style syntax
    # but sending in a query object works fine since they become the same SQL in the end
    pagination_object = db.paginate(
        query, per_page=per_page, page=page, max_per_page=max_per_page
    )

    # We need to send in all parameters back to the HTML template
    # Otherwise data is lost from our filtering/pagination
    return render_template(
        "user/customer/customers.html",
        pagination=pagination_object,
        q=q,
        page=page,
        per_page=per_page,
    )


# länken blir customer.get_one
@customer_bp.route("/<int:id>")
def get_one(id: int):
    customer = db.session.query(Customer).where(Customer.Id == id).first()
    alternative = db.session.get(Customer, id)
    return render_template("user/customer/customer.html", customer=customer)
