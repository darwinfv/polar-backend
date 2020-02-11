from flask import Blueprint, jsonify, request, abort
from passlib.hash import pbkdf2_sha256
import hashlib

import user.db as db
import auth.jwt

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():

    if 'Authorization' in request.headers:
        print(auth.jwt.check_jwt(request.headers.get('Authorization')))

    return 'login route'


@user.route('/register', methods= ['POST'])
def register():
    data = request.get_json()
    register = []
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
        newpass = data['password'] + data['email']
        data['password'] = hashlib.sha512(str.encode(newpass)).hexdigest()


    if len(missing) > 0:
        message = 'Incorrect request, missing' + str(missing)
        abort(400, message)

    user_id = db.create_user(data)

    return jsonify(user_id)




