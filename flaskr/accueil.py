from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required

bp = Blueprint('accueil', __name__, url_prefix='/accueil')

# route pour la page d'accueil /accueil
@bp.route('/')
@login_required
def pageAccueil():

    return render_template('accueil/pageAccueil.html')