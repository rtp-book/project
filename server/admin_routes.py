from flask import jsonify, request, Response, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import flask_login
import logging

log = logging.getLogger(__name__)

admin_api = Blueprint('admin_api', __name__, url_prefix='/api')


class User(flask_login.UserMixin):
    def __init__(self, userid):
        self.id = userid


@admin_api.route('/login', methods=['POST'])
def login():
    record = request.get_json()
    pwd = record.pop('password', "")
    username = record.pop('username', "")
    username = username.lower()

    if validateLogin(username, pwd):
        flask_login.login_user(User(username))
        session.permanent = True
        return jsonify({"OK": 200})
    else:
        log.warning(f"Failed login attempt for user '{username}'")
        flask_login.logout_user()
        return Response("UNAUTHORIZED", 401)


def validateLogin(user, pwd):
    # TODO: Use db.Users table for user validation
    SECRET_PASSWORD = generate_password_hash('123')
    return user == 'admin' and check_password_hash(SECRET_PASSWORD, pwd)


@admin_api.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return jsonify({"OK": 200})


@admin_api.route('/whoami', methods=['GET'])
@flask_login.login_required
def getUser():
    user = ''
    if flask_login.current_user.is_authenticated:
        user = flask_login.current_user.get_id()
    return jsonify({'success': {'user': user}})


@admin_api.route('/ping', methods=['GET'])
@flask_login.login_required
def keepAlive():
    return jsonify({"OK": 200})

