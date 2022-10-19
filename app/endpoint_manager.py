import json
import basicauth
import markdown

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash

from app.auth import login_required
from app.db import get_db, close_db

bp = Blueprint('endpoint_manager', __name__)


def format_endpoint(name):
    endpoint = '/api/fetch/' + name.lower().replace(' ', '_')
    return endpoint


def validate_json(json_data):
    try:
        json.loads(json_data)
        json.dumps(json_data, indent=3)
    except ValueError:
        return False
    return True


@bp.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.execute(
        'SELECT e.id, name, endpoint_base, data, tags, availability, status, created, author_id, username'
        ' FROM endpoints e JOIN user u ON e.author_id = u.id'
        ' WHERE u.id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('endpoint_manager/index.html', endpoints=cursor)
#TODO: disable request limit for admin

@bp.route('/documentation')
@login_required
def documentation():
    with open('README.md', 'r') as f:
        text = f.read()
        mkd_text = markdown.markdown(text)
    return render_template('endpoint_manager/documentation.html', mkd_text=mkd_text)

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        name = request.form['name']
        endpoint_base = format_endpoint(name)
        data = request.form['data']
        availability = request.form['availability']
        status = request.form['status']
        json_validation = request.form['json_validation']
        daily_rate_limit = request.form['daily_rate_limit']
        error = None

        if json_validation == '1' and not validate_json(data):
            error = 'Invalid json.'
        elif json_validation == '1' and validate_json(data):
            data = json.dumps(json.loads(data), indent=3)

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO endpoints'
                    ' (name, endpoint_base, data, availability, status, valid_json, author_id, daily_rate_limit)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (name, endpoint_base, data, availability, status, json_validation, g.user['id'], daily_rate_limit)
                )
                db.commit()
                close_db()
            except db.IntegrityError as err:
                flash(err)
                return redirect(url_for('endpoint_manager.upload'))
            return redirect(url_for('endpoint_manager.index'))

    return render_template('endpoint_manager/upload.html')


def fetch_data(id, check_author=True):
    cursor = get_db().execute(
        'SELECT e.id, name, endpoint_base, data, availability, status, valid_json, '
        ' created, author_id, daily_rate_limit'
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


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    cursor = fetch_data(id)

    if request.method == 'POST':
        name = request.form['name']
        endpoint_base = format_endpoint(name)
        data = request.form['data']
        availability = request.form['availability']
        status = request.form['status']
        json_validation = request.form['json_validation']
        daily_rate_limit = request.form['daily_rate_limit']
        error = None

        if json_validation == '1' and not validate_json(data):
            error = 'Invalid json.'
        else:
            data = json.dumps(json.loads(data), indent=3)

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE endpoints SET name = ?, availability = ?, status = ?, endpoint_base = ?, data = ?, '
                ' valid_json = ?, daily_rate_limit = ?'
                ' WHERE id = ?',
                (name, availability, status, endpoint_base, data, json_validation, daily_rate_limit, id, )
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


@bp.route('/metadata', methods=('GET',))
def metadata():
    # TODO: add state hash --> hash of database for outsiders to check if there has been a state change on data
    cursor = get_db().execute(
        'SELECT name, endpoint_base FROM endpoints WHERE AVAILABILITY = \'Public\' AND STATUS = \'Active\''
    ).fetchall()
    close_db()

    endpoints = {}
    for endpoint in cursor:
        endpoints[endpoint['name']] = endpoint['endpoint_base']

    return endpoints


@bp.route('/api/fetch/<name>', methods=('GET', 'POST',))
def api_fetch(name):
    endpoint_base = format_endpoint(name)

    # TODO: Check for read access
    if request.method == 'GET':
        fetch_id = get_db().execute(
            'SELECT id'
            ' FROM endpoints'
            ' WHERE endpoint_base = ?'
            ' AND STATUS = \'Active\''
            ' AND AVAILABILITY = \'Public\'',
            (endpoint_base,)
        ).fetchone()
        close_db()

        if fetch_id is None:
            return f'Endpoint "{endpoint_base}" not available or set to private.', 404

    elif request.method == 'POST':
        authorization = request.headers.get('Authorization')
        if authorization is not None and "Basic " in authorization:
            client_id, client_secret = basicauth.decode(authorization)
        else:
            return 'Please provide a client id and secret.', 401

        # TODO:  Check for read access
        fetch_id = get_db().execute(
            'SELECT e.id, client_secret'
            ' FROM endpoints e LEFT JOIN client_access c ON e.id = c.endpoint_access_id'
            ' WHERE endpoint_base = ?'
            ' AND STATUS = \'Active\''
            ' AND CURRENT_DATE < DATE_EXPIRY'
            ' AND (AVAILABILITY = \'Public\''
            ' OR (AVAILABILITY = \'Private\' AND c.client_id = ?))',
            (endpoint_base, client_id,)
        ).fetchone()
        close_db()

        if fetch_id is None:
            return f'Endpoint "{endpoint_base}" not available or set to private.', 404
        elif not check_password_hash(fetch_id['client_secret'], client_secret):
            return 'Client not authorised.', 401

    else:
        return 'Method not allowed', 405

    if fetch_id:
        cursor = fetch_data(fetch_id['id'], check_author=False)
        return cursor['data']
    else:
        return error, 401


@bp.route('/api/upload', methods=('POST',))
def api_upload():
    authorization = request.headers.get('Authorization')

    if authorization is not None and "Basic " in authorization:
        client_id, client_secret = basicauth.decode(authorization)
    else:
        return 'Please provide a client id and secret.', 401

    access = get_db().execute(
        'SELECT id, author_id, client_secret FROM client_access'
        ' WHERE client_id = ?'
        ' AND CURRENT_DATE < DATE_EXPIRY'
        ' AND create_access = \'TRUE\'',
        (client_id,)
    ).fetchone()
    close_db()

    if access is None:
        return 'ValueError: name missing.', 400
    elif not check_password_hash(access['client_secret'], client_secret):
        return 'Client not authorised.', 401

    # Check response for values
    if 'name' not in request.get_json():
        return 'ValueError: name missing.', 400
    else:
        name = request.get_json()['name']
        endpoint_base = format_endpoint(name)

    if 'json_validation' not in request.get_json():
        json_validation = 1
    elif request.get_json()['json_validation'] in (0, 1):
        json_validation = request.get_json()['json_validation']
    else:
        return 'ValueError: set json_validation to 0 or 1', 400

    if 'data' not in request.get_json():
        return 'ValueError: data missing.', 400
    else:
        data = request.get_json()['data']
        if json_validation == 1 and not validate_json(json.dumps(data)):
            return 'ValueError: invalid json.', 400
        else:
            data = json.dumps(data, indent=3)

    if 'availability' not in request.get_json():
        availability = 'Public'
    elif request.get_json()['availability'] in ('Public', 'Private'):
        availability = request.get_json()['availability']
    else:
        return 'ValueError: set availability to \'Public\' or \'Private\'', 400

    if 'status' not in request.get_json():
        status = 'Active'
    elif request.get_json()['status'] in ('Active', 'Inactive'):
        status = request.get_json()['status']
    else:
        return 'ValueError: set status to \'Active\' or \'Inactive\'', 400

    if 'daily_rate_limit' not in request.get_json():
        daily_rate_limit = 200
    elif type(request.get_json()['daily_rate_limit']) is int:
        daily_rate_limit = request.get_json()['daily_rate_limit']
    else:
        return 'ValueError: set daily_rate_limit integer value', 400

    db = get_db()
    try:
        db.execute(
            'INSERT INTO endpoints (name, endpoint_base, data, availability, status, '
            ' valid_json, author_id, daily_rate_limit)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, endpoint_base, data, availability, status, json_validation, access['author_id'], daily_rate_limit)
        )
        db.commit()
        close_db()
        return f'Successfully created endpoint: {endpoint_base}'
    except db.IntegrityError as err:
        return err, 400


# TODO: Check if update works when endpoint doesn't exist
@bp.route('/api/update', methods=('PUT',))
def api_update():
    authorization = request.headers.get('Authorization')

    if authorization is not None and "Basic " in authorization:
        client_id, client_secret = basicauth.decode(authorization)
    else:
        return 'Please provide a client id and secret.', 401

    access = get_db().execute(
        'SELECT id, author_id, client_secret FROM client_access'
        ' WHERE client_id = ?'
        ' AND CURRENT_DATE < DATE_EXPIRY'
        ' AND write_access = \'TRUE\'',
        (client_id,)
    ).fetchone()


    if access is None:
        close_db()
        return 'Client not authorised.', 401
    elif not check_password_hash(access['client_secret'], client_secret):
        close_db()
        return 'Client not authorised.', 401

    # Check if endpoint exists
    db = get_db()

        # Check response for values
    if 'name' not in request.get_json():
        close_db()
        return 'ValueError: name missing.', 400
    else:
        name = request.get_json()['name']
        endpoint_base = format_endpoint(name)

    get_result = db.execute(
        'select 1 FROM endpoints'
        ' WHERE endpoint_base = ?',
        (endpoint_base,)
    ).fetchone()

    if get_result is None:
        close_db()
        return f'Endpoint {endpoint_base} does not exist.'
    else:

        # Update json validation or check if it is enabled
        if 'json_validation' not in request.get_json():
            json_validation = get_db().execute(
                'select valid_json from endpoints'
                ' WHERE name = ?',
                (name,)
            ).fetchone()
            json_validation = json_validation['valid_json']
        elif request.get_json()['json_validation'] in (0, 1):
            json_validation = request.get_json()['json_validation']
            db.execute(
                'UPDATE endpoints'
                ' SET valid_json = ?'
                ' WHERE name = ?',
                (json_validation, name,)
            )
            db.commit()
        else:
            close_db()
            return 'ValueError: set json_validation to 0 or 1', 400

        # Update data
        if 'data' not in request.get_json():
            pass
        else:
            data = request.get_json()['data']
            if json_validation == 1 and not validate_json(json.dumps(data)):
                error = 'Invalid json.'
                abort(400, error)
            elif json_validation == 1 and validate_json(json.dumps(data)):
                data = json.dumps(data, indent=3)
            else:
                data = str(data)

            db.execute(
                'UPDATE endpoints'
                ' SET data = ?'
                ' WHERE name = ?',
                (data, name,)
            )
            db.commit()

        # Update availability
        if 'availability' not in request.get_json():
            pass
        elif request.get_json()['availability'] in ('Public', 'Private'):
            availability = request.get_json()['availability']
            db.execute(
                'UPDATE endpoints'
                ' SET availability = ?'
                ' WHERE name = ?',
                (availability, name,)
            )
            db.commit()
        else:
            close_db()
            return 'ValueError: set availability to \'Public\' or \'Private\'', 400

        # Update status
        if 'status' not in request.get_json():
            pass
        elif request.get_json()['status'] in ('Active', 'Inactive'):
            status = request.get_json()['status']
            db.execute(
                'UPDATE endpoints'
                ' SET status = ?'
                ' WHERE name = ?',
                (status, name,)
            )
            db.commit()
        else:
            close_db()
            return 'ValueError: set status to \'Active\' or \'Inactive\'', 400

        # Update daily rate limit
        if 'daily_rate_limit' not in request.get_json():
            pass
        elif type(request.get_json()['daily_rate_limit']) is int:
            daily_rate_limit = request.get_json()['daily_rate_limit']
            db.execute(
                'UPDATE endpoints'
                ' SET daily_rate_limit = ?'
                ' WHERE name = ?',
                (daily_rate_limit, name,)
            )
            db.commit()
        else:
            close_db()
            return 'ValueError: set daily_rate_limit Integer value', 400

        close_db()
        return f'Successfully updated endpoint: {endpoint_base}.'


@bp.route('/api/delete', methods=('DELETE',))
def api_delete():
    authorization = request.headers.get('Authorization')
    error = None

    if authorization is not None and "Basic " in authorization:
        client_id, client_secret = basicauth.decode(authorization)
    else:
        return 'Please provide a client id and secret.', 401

    access = get_db().execute(
        'SELECT id, author_id, client_secret FROM client_access'
        ' WHERE client_id = ?'
        ' AND CURRENT_DATE < DATE_EXPIRY'
        ' AND delete_access = \'TRUE\'',
        (client_id,)
    ).fetchone()
    close_db()

    if access is None:
        return 'Client not authorised.', 401
    elif not check_password_hash(access['client_secret'], client_secret):
        return 'Client not authorised.', 401

    if error is not None:
        return error, 400

    # Check response for values
    if 'name' in request.get_json():
        name = request.get_json()['name']
        endpoint_base = format_endpoint(name)
    elif 'endpoint' in request.get_json():
        endpoint_base = request.get_json()['endpoint']
    else:
        return 'Error: missing endpoint definition', 400

    db = get_db()
    get_result = db.execute(
        'select 1 FROM endpoints'
        ' WHERE endpoint_base = ?',
        (endpoint_base,)
    ).fetchone()

    if get_result is None:
        return f'Endpoint {endpoint_base} does not exist.'
    else:
        db.execute(
            'DELETE FROM endpoints'
            ' WHERE endpoint_base = ?',
            (endpoint_base,)
        )
        db.commit()
        close_db()
        return f'Successfully deleted endpoint: {endpoint_base}'
