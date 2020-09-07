from flask import Blueprint, render_template, request, flash, redirect, session
from flask import current_app as app

from Climber_Carabiner.models import db, User, Route
sess = db.session

# Blueprint configuration
index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@index_bp.route('/', methods=['GET'])
def index():
    """Homepage."""
    return render_template(
        'index.html',
        template='index-template')



