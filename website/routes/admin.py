from flask import Blueprint, render_template, jsonify,request,url_for
from flask_login import login_required,current_user
from website.models import Event
import stripe
from website import STRIPE_PUBLISHABLE_KEY

admin = Blueprint('admin' , __name__)

@admin.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    events = Event.query.filter_by(admin_id=current_user.id).all()
    return render_template('organizer/organizer.html',events=events)

@admin.route('/admin/add-card', methods=['GET'])
def admin_add_card():
    # Create a Stripe customer if one doesn't exist
    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(email=f"admin{current_user.id}@example.com")
        current_user.stripe_customer_id = customer.id

    # Create a Stripe Checkout session to collect card
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="setup",
        customer=current_user.stripe_customer_id,
        success_url=url_for('card_added_success', _external=True),
        cancel_url=url_for('admin_add_card', _external=True)
    )

    return render_template("buyTicket.html", checkout_session_id=session.id, stripe_key=STRIPE_PUBLISHABLE_KEY)

@admin.route('/admin/card-added-success')
def card_added_success():
    return "Card added successfully!"
