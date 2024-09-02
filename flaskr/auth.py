import functools
import uuid

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from . import mongo

bp = Blueprint('auth', __name__, url_prefix='/auth')


# route pour l'inscription /auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Un username est nécessaire.'
        elif not password:
            error = 'Un mot de passe est nécessaire.'

#si le formulaire est bon, on crée le user
        if error is None:
            try:
                user = mongo.db.users.find_one({'username': username})
                if user is not None:
                    flash('L\'utilisateur {} existe déjà.'.format(username))
                else:
                    userID = uuid.uuid4()
                    mongo.db.users.insert_one({'username': username, 'password': generate_password_hash(password), 'userID': str(userID)})
                    print('Utilisateur créé')
                    return redirect(url_for("auth.login"))
            except:
                error = 'Erreur lors de la création de l\'utilisateur'
                flash(error)
            else:
                return redirect(url_for("auth.register"))

    return render_template('auth/register.html')

# route pour la connexion /auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        #vérifie que l'utilisateur existe et que le mot de passe est correct
        user = mongo.db.users.find_one({'username': username})

        if user is None:
            error = 'Cet utilisateur n\'existe pas.'
        elif not check_password_hash(user['password'], password):
            error = 'Mot de passe incorrect.'

        # si il n'y a pas d'erreur, on connecte l'utilisateur
        if error is None:
            session.clear()
            session['userID'] = user['userID']
            print(session['userID'])
            return redirect(url_for('accueil.pageAccueil'))

        flash(error)

    return render_template('auth/login.html')


# avant chaque requête, on vérifie si l'utilisateur est connecté pour vérifier s'il a accès à certaines pages
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userID')

    if user_id is None:
        g.user = None
    else:
        g.user = mongo.db.users.find_one({'userID': user_id},{'password': 0, '_id': 0})

#déconnexion de l'utilisateur
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# vérifie si l'utilisateur est connecté avant d'accéder à certaines pages
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Vous devez être connecté pour accéder à cette page.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view













