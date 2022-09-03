import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db, close_db

bp = Blueprint('endpoint_manager', __name__)

@bp.route('/')
def index():
    db = get_db()
    cursor = db.execute(
        'SELECT e.id, name, data, tags, access, created, author_id, username'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('endpoint_manager/index.html', endpoints=cursor)

#TODO: add check json validity on upload else flash error
#TODO: add actual specified endpoint
@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        name = request.form['name']
        data = request.form['data']
        access = request.form['access']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO endpoints (name, data, access, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (name, data, access, g.user['id'])
            )
            db.commit()
            return redirect(url_for('endpoint_manager.index'))

    return render_template('endpoint_manager/upload.html')

def fetch_data(id, check_author=True):
    cursor = get_db().execute(
        'SELECT e.id, access, name, data, created, author_id, username'
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
        data = request.form['data']
        access = request.form['access']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE endpoints SET access = ?, name = ?, data = ?'
                ' WHERE id = ?',
                (access, name, data, id)
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
    if request.method == 'GET':
        fetch_id = get_db().execute(
            'SELECT id FROM endpoints WHERE name = ? AND ACCESS = \'Public\'',
            (name,)
        ).fetchone()
        close_db()

    elif request.method == 'POST':
        abort(404, f"Private endpoint querying not enabled yet.")

    # TODO: Add private endpoint querying for whitelisted tokens
    if fetch_id is None:
        abort(404, f"Endpoint api/{name} doesn\'t exist.")
    else:
        cursor = fetch_data(fetch_id['id'], check_author=False)
        return cursor['data']

#TODO: Change name to actual full fletched endpoint
@bp.route('/metadata', methods=('GET',))
def metadata():
    cursor = get_db().execute(
        'SELECT name FROM endpoints WHERE ACCESS = \'Public\''
    ).fetchall()
    close_db()

    endpoints = {}
    for endpoint in cursor:
        endpoints[endpoint['name']] = endpoint['name']

    return endpoints

