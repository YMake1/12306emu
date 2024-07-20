from flask import Blueprint, render_template

error_blu = Blueprint('error_blu', __name__)

@error_blu.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404