from flask import Blueprint, render_template, jsonify,request
from flask_login import login_required,current_user
from website.models import Event

admin = Blueprint('admin' , __name__)

@admin.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    events = Event.query.filter_by(admin_id=current_user.id).all()
    return render_template('organizer/organizer.html',events=events)
