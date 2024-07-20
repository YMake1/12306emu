from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

deco_blu = Blueprint('deco_blu', __name__)

@deco_blu.route('/home/<user_id>')
@login_required
def home(user_id):
    if str(current_user.id) == user_id:
        return render_template('main/home.html', user_name=current_user.name)
    else:
        flash('You are not authorized to view this page.')
        return redirect(url_for('home', user_id=str(current_user.id)))