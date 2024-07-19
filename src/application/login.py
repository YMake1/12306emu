import os
from flask import Blueprint, current_app, request, redirect, url_for, flash, render_template, make_response
from flask_login import login_user
from werkzeug.security import generate_password_hash
from src.database import models
from configs import project_root

login_blu=Blueprint('login_blu', __name__)
login_blu.template_folder = os.path.join(project_root, 'templates')
login_blu.static_folder = os.path.join(project_root, 'static')

@login_blu.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            flash('user not found, please register')
            current_app.logger.info('user not found')
            return redirect(url_for('login_blu.signup'))
        else:
            if user.validate_password(password):
                flash('login successful')
                login_user(user)
                current_app.logger.info('login successful')
                return redirect(url_for('home', user_id=str(user.id)))
            else:
                flash('incorrect password')
                current_app.logger.info('incorrect password')
                return redirect(url_for('login_blu.login'))
    if request.method == 'GET':
        try:
            current_app.logger.info('login page accessed')
            return render_template('login/login.html')
        except Exception as e:
            current_app.logger.error(e)
            return make_response(render_template('login/login.html'), 500)

@login_blu.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        user = models.User(name=name, email=email, gender=gender, password_hash=generate_password_hash(password))
        models.db.session.add(user)
        models.db.session.commit()
        flash('signup successful')
        return redirect(url_for('login_blu.login'))
    return render_template('login/signup.html')