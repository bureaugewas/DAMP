import json

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
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO endpoints (name, endpoint_base, data, access, status, author_id)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (name, endpoint_base, data, access, status, g.user['id'])
                )
                db.commit()
            except:
                flash('Endpoint name already exists')
                return redirect(url_for('endpoint_manager.upload'))
            return redirect(url_for('endpoint_manager.index'))

    return render_template('endpoint_manager/upload.html')

def fetch_data(id, check_author=True):
    cursor = get_db().execute(
        'SELECT e.id, name, endpoint_base, data, access, status, created, author_id, username'
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
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE endpoints SET name = ?, access = ?, status = ?, endpoint_base = ?, data = ?'
                ' WHERE id = ?',
                (name, access, status, endpoint_base, data, id,)
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

@bp.route('/api/<name>', methods=('GET', 'POST'))
def api(name):
    endpoint_base = format_endpoint(name)
    if request.method == 'GET':
        fetch_id = get_db().execute(
            'SELECT id FROM endpoints WHERE endpoint_base = ? AND ACCESS = \'Public\' AND STATUS = \'Active\'',
            (endpoint_base,)
        ).fetchone()
        close_db()

    elif request.method == 'POST':
        abort(404, f"Private endpoint querying not enabled yet.")

    # TODO: Add private endpoint querying for whitelisted tokens
    if fetch_id is None:
        abort(404, f"Endpoint {endpoint_base} doesn\'t exist.")
    else:
        cursor = fetch_data(fetch_id['id'], check_author=False)
        return cursor['data']

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

