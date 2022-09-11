import json
import basicauth
from werkzeug.security import check_password_hash

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db, close_db

bp = Blueprint('endpoint_manager', __name__)

def format_endpoint(name):
    endpoint = '/api/' + name.lower().replace(' ', '_')
    return endpoint

def validate_json(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

@bp.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.execute(
        'SELECT e.id, name, endpoint_base, data, tags, access, status, created, author_id, username'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' WHERE u.id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('endpoint_manager/index.html', endpoints=cursor)

#TODO: add check json validity on upload else flash error
@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        name = request.form['name']
        endpoint_base = format_endpoint(name)
        data = request.form['data']
        access = request.form['access']
        status = request.form['status']
        json_validation = request.form['json_validation']
        error = None

        if json_validation == '1' and not validate_json(data):
            error = 'Invalid json.'

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO endpoints (name, endpoint_base, data, access, status, valid_json, author_id)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (name, endpoint_base, data, access, status, json_validation, g.user['id'],)
                )
                db.commit()
            except:
                flash('Endpoint name already exists')
                return redirect(url_for('endpoint_manager.upload'))
            return redirect(url_for('endpoint_manager.index'))

    return render_template('endpoint_manager/upload.html')

def fetch_data(id, check_author=True):
    cursor = get_db().execute(
        'SELECT e.id, name, endpoint_base, data, access, status, valid_json, created, author_id'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()
    close_db()

    if cursor is None:
        abort(404, f"Endpoint id {id} doesn't exist.")

    if check_author and cursor['author_id'] != g.user['id']:
        abort(403)

    return cursor

#TODO: add check json on upload else flash error
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    cursor = fetch_data(id)

    if request.method == 'POST':
        name = request.form['name']
        endpoint_base = format_endpoint(name)
        data = request.form['data']
        access = request.form['access']
        status = request.form['status']
        json_validation = request.form['json_validation']
        error = None

        if json_validation == '1' and not validate_json(data):
            error = 'Invalid json.'

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE endpoints SET name = ?, access = ?, status = ?, endpoint_base = ?, data = ?, valid_json = ?'
                ' WHERE id = ?',
                (name, access, status, endpoint_base, data, json_validation, id, )
            )
            db.commit()
            return redirect(url_for('endpoint_manager.index'))

    return render_template('endpoint_manager/update.html', endpoint=cursor)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    fetch_data(id)
    db = get_db()
    db.execute('DELETE FROM endpoints WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('endpoint_manager.index'))

@bp.route('/api/<name>', methods=('GET','POST',))
def api(name):
    endpoint_base = format_endpoint(name)
    error = None

    if request.method == 'GET':
        fetch_id = get_db().execute(
            'SELECT id'
            ' FROM endpoints'
            ' WHERE endpoint_base = ?'
            ' AND STATUS = \'Active\''
            ' AND ACCESS = \'Public\'',
            (endpoint_base,)
        ).fetchone()
        close_db()

        if fetch_id is None:
            error = f'Endpoint "{endpoint_base}" not available or set to private.'

    elif request.method == 'POST':
        authorization = request.headers.get('Authorization')
        if authorization is not None and "Basic " in authorization:
            client_id, client_secret = basicauth.decode(authorization)
        else:
            error = 'Please provide a client id and secret.'

        fetch_id = get_db().execute(
            'SELECT e.id, client_secret'
            ' FROM endpoints e LEFT JOIN client_access c ON e.id = c.endpoint_access_id'
            ' WHERE endpoint_base = ?'
            ' AND STATUS = \'Active\''
            ' AND (ACCESS = \'Public\''
            ' OR (ACCESS = \'Private\' AND c.client_id = ?))',
            (endpoint_base, client_id,)
        ).fetchone()
        close_db()

        if fetch_id is None:
            error = f'Endpoint {endpoint_base} not available or set to private.'
        elif not check_password_hash(fetch_id['client_secret'], client_secret):
            error = 'Client not authorised.'

    if error is None:
        cursor = fetch_data(fetch_id['id'], check_author=False)
        return cursor['data']
    else:
        abort(400, error)

@bp.route('/metadata', methods=('GET',))
def metadata():
    cursor = get_db().execute(
        'SELECT name, endpoint_base FROM endpoints WHERE ACCESS = \'Public\' AND STATUS = \'Active\''
    ).fetchall()
    close_db()

    endpoints = {}
    for endpoint in cursor:
        endpoints[endpoint['name']] = endpoint['endpoint_base']

    return endpoints

