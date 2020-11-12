from flask import jsonify, request, Blueprint
import flask_login
import logging

import dbutils as db

log = logging.getLogger(__name__)

db_api = Blueprint('db_api', __name__, url_prefix='/api')


LOOKUPS = ['Categories', 'Publishers', 'Conditions', 'Formats']


@db_api.route('/lookup/<string:name>', methods=['GET'])
def get_lookup(name):

    if name in LOOKUPS:
        result, data = db.select(f"SELECT * FROM {name}")
        return jsonify({result: data})

    return jsonify(None)


@db_api.route('/lookup/<string:name>', methods=['POST'])
@flask_login.login_required
def update_lookup(name):
    if name in LOOKUPS:
        record = request.get_json()
        record_id = record.pop('ID', None)
        fields = record.keys()
        values = tuple([record[field] for field in fields])

        if record_id:
            fields = ','.join([f"{field}=?" for field in fields])
            sql = f"UPDATE {name} SET {fields} WHERE ID=?"
            values = values + (record_id,)
        else:
            fields = ','.join(record.keys())
            params = ','.join(['?']*len(record.keys()))
            sql = f"INSERT INTO {name} ({fields}) VALUES ({params})"

        result, data = db.execute(sql, values)

        return jsonify({result: data})

    return jsonify(None)


@db_api.route('/lookup/<string:name>', methods=['DELETE'])
@flask_login.login_required
def delete_lookup(name):
    if name in LOOKUPS:
        record = request.get_json()
        record_id = record.pop('ID', None)

        if record_id:
            sql = f"DELETE FROM {name} WHERE ID=?"
            values = (record_id,)
            result, data = db.execute(sql, values)
            return jsonify({result: data})

    return jsonify(None)


@db_api.route('/book', methods=['GET'])
def get_book():
    book_id = request.args.get('id', "")
    if len(book_id) > 0:
        result, data = db.select(f"SELECT * FROM Books WHERE ID=?", (book_id,))
        return jsonify({result: data[0]} if len(data) > 0 else None)

    return jsonify(None)


@db_api.route('/book', methods=['POST'])
@flask_login.login_required
def update_book():
    record = request.get_json()
    if record:
        record_id = record.pop('ID', None)
        fields = record.keys()
        values = tuple([record[field] if len(f"{record[field]}") > 0 else None 
                        for field in fields]
                       )

        if record_id:
            fields = ','.join([f"{field}=?" for field in fields])
            sql = f"UPDATE Books SET {fields} WHERE ID=?"
            values = values + (record_id,)
        else:
            fields = ','.join(record.keys())
            params = ','.join(['?']*len(record.keys()))
            sql = f"INSERT INTO Books ({fields}) VALUES ({params})"

        result, data = db.execute(sql, values)
        return jsonify({result: data})

    return jsonify(None)


@db_api.route('/book', methods=['DELETE'])
@flask_login.login_required
def delete_book():
    record = request.get_json()
    if record:
        record_id = record.pop('ID', None)

        if record_id:
            sql = f"DELETE FROM Books WHERE ID=?"
            values = (record_id,)
            result, data = db.execute(sql, values)
            return jsonify({result: data})

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

    values = tuple([params[field] if len(f"{params[field]}") > 0 else None 
                    for field in fields]
                   )
    
    def get_operator(field):
        return ' LIKE ' if field in ['Title', 'Author'] else '='
    
    wc = ' AND '.join([f"{field}{get_operator(field)}?" for field in fields])
    if len(wc) > 0:
        wc = f" WHERE {wc}"
    result, data = db.select(f"SELECT * FROM Books{wc}", values)
    return jsonify({result: data} if len(data) > 0 else None)

