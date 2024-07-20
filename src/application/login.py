import os
from flask import Blueprint, request, redirect, url_for, flash, render_template, make_response
from flask import current_app as app
from flask_login import login_user
from werkzeug.security import generate_password_hash

from src.database import models
from configs import project_root

login_blu=Blueprint('login_blu', __name__)
login_blu.template_folder = os.path.join(project_root, 'templates')
login_blu.static_folder = os.path.join(project_root, 'static')

@login_blu.route('/login', methods=['GET', 'POST'])
def login():
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            flash('user not found, please register')
            app.logger.info('user not found')
            return redirect(url_for('login_blu.signup'))
        else:
            if user.validate_password(password):
                flash('login successful')
                login_user(user)
                app.logger.info(f'login successful {ip_address}')
                return redirect(url_for('deco_blu.home', user_id=str(user.id)))
            else:
                flash('incorrect password')
                app.logger.info('incorrect password')
                return redirect(url_for('login_blu.login'))
    if request.method == 'GET':
        try:
            app.logger.info(f'login page accessed {ip_address}')
            return render_template('login/login.html')
        except Exception as e:
            app.logger.error(e)
            return make_response(render_template('login/login.html'), 500)

@login_blu.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        id_number = request.form.get('id_number')
        user = models.User(name=name, email=email, phone_number=phone_number, id_number=id_number, gender=gender, password_hash='temp')
        user.set_password(password)
        models.db.session.add(user)
        models.db.session.commit()
        flash('signup successful')
        app.logger.info(f'signup successful {ip_address}')
        return redirect(url_for('login_blu.login'))
    app.logger.info(f'signup page accessed {ip_address}')
    return render_template('login/signup.html')