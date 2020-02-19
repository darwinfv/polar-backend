from flask import Blueprint, jsonify, request, abort, g
import hashlib

import user.db as db
import auth
import auth.jwt
import uuid

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        abort(400, "Missing credentials")

    data['password'] = auth.hash_password(data['password'], data['email'])
    
    res = db.login(data)

    jwt = auth.jwt.make_jwt(res[0])
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'auth': jwt,
        'permissions': 'n',
    }
    return resp


@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    missing = []

    if 'firstName' not in data:
        missing.append('firstName')

    if 'lastName' not in data:
        missing.append('lastName')

    if 'email' not in data:
        missing.append('email')

    if 'password' not in data:
        missing.append('password')
    else:
        data['password'] = auth.hash_password(data['password'], data['email'])

    if len(missing) > 0:
        message = 'Incorrect request, missing ' + str(missing)
        abort(400, message)

    user_id = db.create_user(data)
    jwt = auth.jwt.make_jwt(user_id)
    resp = {
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'auth': jwt,
        'permissions': 'n',
    }

    return resp


@user.route('/getInfo', methods=['POST'])
@auth.login_required(perms=None)
def getInfo():
    res = db.getInfo(g.userId)
    
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'email': res[3],
        'phone': res[4]
    }

    return resp


@user.route('/setInfo', methods=['POST'])
@auth.login_required(perms=None)
def setInfo():
    data = request.get_json()
    data['userId'] = g.userId

    if 'firstName' not in data or 'lastName' not in data or 'phone' not in data:
        abort(400, "Missing data")

    res = db.setInfo(data)
    return {}


@user.route('/delete', methods=['POST'])
@auth.login_required(perms=None)
def delete():
    # db.delete(data)
    return 'deleted'
    