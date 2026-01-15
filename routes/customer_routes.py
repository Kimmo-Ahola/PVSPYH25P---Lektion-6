from flask import Blueprint, render_template
from database import db
from models.model import Customer

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")


# länken blir customer.get_all
@customer_bp.route("/")
def get_all():
    customers = db.session.query(Customer).all()
    return render_template("user/customer/customers.html", customers=customers)


# länken blir customer.get_one
@customer_bp.route("/<int:id>")
def get_one(id: int):
    customer = db.session.query(Customer).where(Customer.Id == id).first()
    alternative = db.session.get(Customer, id)
    return render_template("user/customer/customer.html", customer=customer)
