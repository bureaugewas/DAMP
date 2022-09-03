from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('endpoint_manager', __name__)

@bp.route('/')
def index():
    db = get_db()
    endpoints = db.execute(
        'SELECT e.id, name, data, tags, access, created, author_id, username'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('endpoint_manager/index.html', endpoints=endpoints)

#TODO: add check json validity on upload else flash error
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

def get_endpoint(id, check_author=True):
    endpoint = get_db().execute(
        'SELECT e.id, access, name, data, created, author_id, username'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()

    if endpoint is None:
        abort(404, f"Endpoint id {id} doesn't exist.")

    if check_author and endpoint['author_id'] != g.user['id']:
        abort(403)

    return endpoint

#TODO: add check json on upload else flash error
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    endpoint = get_endpoint(id)

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

    return render_template('endpoint_manager/update.html', endpoint=endpoint)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_endpoint(id)
    db = get_db()
    db.execute('DELETE FROM endpoints WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('endpoint_manager.index'))