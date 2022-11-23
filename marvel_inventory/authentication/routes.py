from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_inventory.forms import UserLoginForm
from marvel_inventory.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder= 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            
            user = User(email, first_name, last_name, password = password)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f"You have successfully created a User account {email}", "user-created")
            
            return redirect(url_for('auth.signin'))
    
    except:
        raise Exception('Invalid Form Data')
            
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            
            logged_user = User.query.filter(User.email == email).first()
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully loggged in via Email/Password', "auth-success")
                return redirect(url_for('site.profile'))
            
            else:
                flash("Your email and password are invalid.", "auth-failed")
                return redirect(url_for('auth.signin'))
            
    except:
        raise Exception("Invalid Form Data")

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))