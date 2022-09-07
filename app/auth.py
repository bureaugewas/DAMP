import functools
import os
import secrets
import datetime
from datetime import timedelta, date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db, close_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/client_access', methods=('GET', 'POST'))
@login_required
def client_access():
    cursor_generate = get_db().execute(
        'SELECT id, endpoint_base, access FROM endpoints ',
        ()
    ).fetchall()
    close_db()

    cursor_delete = get_db().execute(
        'SELECT c.id as token_id, client_id, endpoint_base,  c.daily_rate_limit, date(c.date_created) as date_created,'
        'date(c.date_expiry) as date_expiry'
        ' FROM endpoints e LEFT JOIN client_access c ON e.id = c.endpoint_access_id',
        ()
    ).fetchall()
    close_db()

    if request.method == 'POST' and request.form['submit'] == 'Generate':
        client_id = secrets.token_hex(16)
        client_token = secrets.token_hex(32)
        endpoint_access_id = request.form['endpoint_access_id']
        access_limit = request.form['access_limit']
        daily_rate_limit = request.form['daily_rate_limit']
        db = get_db()
        error = None

        if not client_id and client_token:
            error = 'Error during generation of client id or client token'
        if not endpoint_access_id:
            error = 'Specifying endpoint is required.'
        if not access_limit or access_limit == 'default' or access_limit == '':
            access_limit = 99999
        if not daily_rate_limit or daily_rate_limit == 'default' or daily_rate_limit == '':
            daily_rate_limit = 99999

        date_created = date.today()
        date_expiry = date_created + datetime.timedelta(days=int(access_limit))

        if error is None:
            try:
                db.execute(
                    "INSERT INTO client_access (author_id, client_id, client_token, endpoint_access_id,date_created, date_expiry, daily_rate_limit)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (g.user['id'], client_id, generate_password_hash(client_token),endpoint_access_id,date_created,date_expiry,daily_rate_limit),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Database error, try again"
            else:
                flash('Client id: ' + client_id)
                flash('Client token: ' + client_token)
                return redirect(url_for("auth.client_access"))

        flash(error)

    elif request.method == 'POST' and request.form['submit'] == 'Delete':
        client_id = request.form['delete_token']
        db = get_db()
        db.execute('DELETE FROM client_access WHERE client_id = ?', (client_id,))
        db.commit()
        flash('Deleted client token: ' + client_id)
        return redirect(url_for("auth.client_access"))

    return render_template('auth/client_access.html', endpoints=cursor_generate, tokens=cursor_delete)