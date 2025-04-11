from flask import render_template,request,flash,redirect,url_for,Blueprint
from .models import User
from . import db
from flask_login import logout_user,login_required,login_user
from werkzeug.security import generate_password_hash,check_password_hash

forms = Blueprint('forms', __name__)

#registration page route
@forms.route('/register', methods =["POST","GET"])
def register():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        with db.Session(db.engine) as session:
            user = session.query(db.User).filter_by(email=email).first()

        user = User.query.filter_by(email=email).first()    
        if user:
            flash("email already exists",category='error')
            return redirect(url_for('register'))
        
        with db.Session(db.engine) as session:
            new_user = db.User(email=email,password=generate_password_hash(password))
            session.add(new_user)
            session.commit()

        flash("Registration complete.Please login","success")
        return redirect(url_for("login"))

    return render_template('register.html')


#login page route
@forms.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email=request.form.get('email') 
        password=request.form.get('password')
        with db.Session(db.engine) as session:
            user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', category='error')

    return render_template('login.html')


#logout page route
@forms.route('/logout',methods=[ 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('forms.login'))
