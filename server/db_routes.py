from flask import jsonify, request, Blueprint
import flask_login
import logging
from datetime import date, datetime

import dbutils as db
from dataModel import get_model, Books

log = logging.getLogger(__name__)

db_api = Blueprint('db_api', __name__, url_prefix='/api')

LOOKUPS = ['Categories', 'Publishers', 'Conditions', 'Formats']


@db_api.route('/lookup/<string:name>', methods=['GET'])
def get_lookup(name):
    if name in LOOKUPS:
        try:
            model = get_model(name)
            with db.session_scope() as session:
                result = session.query(model).all()
                rows = [db.todict(row) for row in result]
                return jsonify({'success': rows} if rows is not None else None)
        except Exception as e:
            log.error(e)
            return jsonify({'error': str(e)})

    return jsonify(None)


@db_api.route('/lookup/<string:name>', methods=['POST', 'DELETE'])
@flask_login.login_required
def update_lookup(name):
    if name in LOOKUPS:
        model = get_model(name)
        record = request.get_json()
        if request.method == 'POST':
            return jsonify(db.update_record(model, record))
        elif request.method == 'DELETE':
            return jsonify(db.delete_record(model, record))

    return jsonify(None)


@db_api.route('/book', methods=['GET'])
def get_book():
    book_id = request.args.get('id', "")
    if len(book_id) > 0:
        try:
            with db.session_scope() as session:
                row = session.query(Books).filter(Books.ID == book_id).first()
                record = book_fixup(db.todict(row))
                return jsonify({'success': record} if row is not None else None)
        except Exception as e:
            log.error(e)
            return jsonify({'error': str(e)})

    return jsonify(None)


@db_api.route('/book', methods=['POST', 'DELETE'])
@flask_login.login_required
def update_book():
    record = request.get_json()
    if record:
        if request.method == 'POST':

            # Incoming Fixup
            record = {key: val if len(f"{val}") > 0 else None for key, val in record.items()}
            if record['DateAcquired'] is not None:
                record['DateAcquired'] = datetime.strptime(record['DateAcquired'], "%Y-%m-%d")

            return jsonify(db.update_record(Books, record))
        elif request.method == 'DELETE':
            return jsonify(db.delete_record(Books, record))

    return jsonify(None)


@db_api.route('/books', methods=['GET'])
def get_books():
    params = dict(request.args)
    fields = params.keys()

    if 'IsFiction' in fields:
        params['IsFiction'] = int(params['IsFiction'])
    if 'Title' in fields:
        params['Title'] = f"%{params['Title']}%"
    if 'Author' in fields:
        params['Author'] = f"%{params['Author']}%"

    filter_cols = [field for field in fields if len(f"{params[field]}") > 0]
    try:
        with db.session_scope() as session:
            query = session.query(Books)
            for col in filter_cols:
                if col in ['Title', 'Author']:
                    query = query.filter(getattr(Books, col).like(params[col]))
                else:
                    query = query.filter(getattr(Books, col) == params[col])

            result = query.all()
            rows = [book_fixup(db.todict(row)) for row in result]
            return jsonify({'success': rows} if rows is not None else None)
    except Exception as e:
        log.error(e)
        return jsonify({'error': str(e)})


def book_fixup(record: dict) -> dict:
    # Fix Date and Boolean mismatches from DB
    record['IsFiction'] = 1 if record['IsFiction'] else 0
    if record['DateAcquired'] is not None:
        record['DateAcquired'] = date.strftime(record['DateAcquired'], "%Y-%m-%d")

    return record
