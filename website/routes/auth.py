from flask import render_template,request,flash,redirect,url_for,Blueprint,session
from website.models import Customer
from website import db,mail
from flask_login import logout_user,login_required,login_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from website.forms.auth_forms import ResetRequestForm,ResetPasswordForm
from flask_mail import Message


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
        login_user(new_user, remember=True)

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
@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@yourdomain.com",
                  recipients=[user.email])
    reset_url = url_for('auth.reset_token', token=token, _external=True)
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)  # same as before
        flash('If that email exists, you will receive a reset link shortly.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Customer.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Password updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form=form)

@auth.route('/edit-profile', methods=['POST'])
def edit_profile():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')

    # Update user
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.email = email
    current_user.phone_number = phone_number

    db.session.commit()
    flash('Profile updated successfully!', category='success')

    return redirect(url_for('views.profile'))









