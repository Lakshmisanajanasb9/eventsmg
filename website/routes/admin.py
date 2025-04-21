from flask import Blueprint, render_template, jsonify,request
from flask_login import login_required

admin = Blueprint('admin' , __name__)

@admin.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    return render_template('organizer/organizer.html')
