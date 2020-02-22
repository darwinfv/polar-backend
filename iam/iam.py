from flask import Blueprint, jsonify, request, abort, g

import iam.db as db
import auth
import auth.jwt
import auth.perms

iam = Blueprint('iam', __name__)


@iam.route('/createRole', methods=['POST'])
@auth.login_required(perms=[11])
def createRole():
    data = request.get_json()
    if 'roleName' not in data or 'permissions' not in data:
        abort(400, "Missing data")
    db.createRole(data)
    return jsonify()


@iam.route('/removeRole', methods=['POST'])
@auth.login_required(perms=[11])
def removeRole():
    data = request.get_json()
    if 'roleId' not in data:
        abort(400, "Missing data")
    db.removeRole(data['roleId'])
    return jsonify()


@iam.route('/assignRole', methods=['POST'])
@auth.login_required(perms=[11])
def assignRole():
    data = request.get_json()
    if 'roleId' not in data or 'userId' not in data:
        abort(400, "Missing data")
    db.assignRole(data)
    return jsonify()


@iam.route('/revokeRole', methods=['POST'])
@auth.login_required(perms=[11])
def revokeRole():
    data = request.get_json()
    if ('roleId') not in data or 'userId' not in data:
        abort(400, "Missing data")
    db.revokeRole(data)
    return jsonify()


@iam.route('/permissions', methods=['POST'])
def permissions():
    perms = db.permissions()
    resp = {}
    for perm in perms:
        resp[perm[0]] = perm[1]
    return jsonify(resp)


@iam.route('/getRoles', methods=['POST'])
@auth.login_required(perms=[11])
def getRoles():
    roles = db.getAllRoles()
    out  = {}

    for row in roles:
        if row[0] not in out:
            role = {}
            role['key'] = row[0]
            role['roleName'] = row[1]
            role['permissions'] = [row[2]]
            out[row[0]] = role
        else:
            out[row[0]]['permissions'].append(row[2])

    return jsonify(list(out.values()))


@iam.route('/getUserRoles', methods=['POST'])
@auth.login_required(perms=[11])
def getUserRoles():
    users = db.getAllUserRoles()
    out = {}

    for row in users:  
        if row[0] not in out:
            user = {}
            user['key'] = row[0]
            user['firstName'] = row[1]
            user['lastName'] = row[2]
            user['phone'] = row[3]
            user['email'] = row[4]
            user['roles'] = [row[5]]
            out[row[0]] = user
        else:
            out[row[0]]['roles'].append(row[5])

    return jsonify(list(out.values()))