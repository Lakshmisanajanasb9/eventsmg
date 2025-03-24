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

        #extracts data ofthe user in the form
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        #compares details of the data inputted and the existing data in database
        user = User.query.filter_by(email=email).first()    
        if user:
            #validation
            flash("email already exists",category='error')
        elif len(username) < 5 :
            flash("Error: username must be greater than 4 characters",category='error')
        elif len(password)  < 7 :
            flash("Error: password must be greater than 6 characters",category='error')
        elif len(password)  > 21 :
            flash("Error: password must be less then 20 characters",category='error')
        elif not any(char.isdigit() for char in password):     #checks if the password contains numbers
            flash("Error : PAssword does not contain at least 1 number",category='error')
        elif not any(char.isupper() for char in password):      #checks if the password contains uppercases
            flash("Error :password does not contain at least 1 upper case letter",category='error')
        elif not any(char.islower() for char in password):      #checks if the password contains lowercases
            flash("Error :password does not contain at least 1 lower case letter ",category='error')
        else:
            new_user = User(email=email, username=username,password=generate_password_hash(password))
            flash('Account created',category='success')
            #will add a new row to the database using the data entered
            db.session.add(new_user)
            db.session.commit()

            #the user will be redirected to the home screen after signing up
            return redirect(url_for('views.display_manga'))
    
    return render_template('register.html')


#login page route
@forms.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email=request.form.get('email') 
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user, remember=True)
            return redirect(url_for('views.display_manga'))
        else:
            flash('email does not exist', category='error')
    else:
        flash('Email does not exist', category="error")

    return render_template('login.html')


#logout page route
@forms.route('/logout',methods=[ 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('forms.login'))
