import stripe
from flask import Blueprint, render_template, jsonify,request
from website.models import Event 

payment = Blueprint('payment' , __name__)

@payment.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    event_id = request.form.get('event_id')
    tickets = int(request.form.get('tickets', 1))
    
    # Get event from database
    event = Event.query.get_or_404(event_id)
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': event.title,
                        'description': f'Event on {event.date.strftime("%Y-%m-%d")}',
                    },
                    'unit_amount': int(event.price * 100),
                },
                'quantity': tickets,
            }],
            mode='payment',
            success_url=url_for('payment_success', _external=True) + 
                        '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment_cancel', _external=True),
            metadata={
                'event_id': event_id,
                'user_id': session.get('user_id'),
                'tickets': tickets
            }
        )
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403
