from flask import render_template,request,flash,redirect,url_for,Blueprint
from website.models import Customer
from website import db
from flask_login import logout_user,login_required,login_user
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint('auth', __name__)

#registration page route
@auth.route('/register', methods =["POST","GET"])
def register():
    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")

        user_email = Customer.query.filter_by(email=email).first()    
        user_phone = Customer.query.filter_by(phone=phone_number).first()

        if user_email:
            flash("email already exists",category='error')
            return redirect(url_for('register'))
        if user_phone:
            flash("phone is already linked to other account",catergory='error')
            return redirect(url_for('register'))

        new_user = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone_number,
            password=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration complete","success")
        return redirect(url_for("views.home"))

    return render_template('auth.register')

#login page route
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email=request.form.get('email') 
        password=request.form.get('password')

        user = Customer.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', category='error')

    return render_template('login.html')

#logout page route
@auth.route('/logout',methods=[ 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('forms.login'))
