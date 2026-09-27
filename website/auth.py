from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

        flash('Invalid email or password.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        first_name = (request.form.get('firstName') or '').strip()
        password1 = request.form.get('password1') or ''
        password2 = request.form.get('password2') or ''

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists.', category='error')
        elif len(email) < 4 or '@' not in email:
            flash('Please enter a valid email address.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()

            # Authenticate the user object that was just created. The previous
            # implementation attempted to log in the pre-registration lookup,
            # which is None for a new account.
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
