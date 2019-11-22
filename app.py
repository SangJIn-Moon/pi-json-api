import subprocess
import re
import os
from flask import Flask
from flask import request

import api.parsers.users
import api.actions.users
import api.parsers.groups
import api.actions.groups
import api.parsers.misc

app = Flask(__name__)

version = '0.1.0'


def res(data={}, status=True):
    obj = {
        'version': version,
        'status': 'ok' if True else 'error'
    }
    obj.update(data)
    return obj


@app.route('/')
def index():
    return res()


# user probes and actions
@app.route('/users')
def users():
    return res({'users': api.parsers.users.parse()})


@app.route('/user/<uid>')
def user(uid):
    return res({'user': api.parsers.users.parse_single(uid)})


@app.route('/useradd', methods=['POST'])
def useradd():
    data = request.get_json()
    response = api.actions.users.create(
        data['name'], data['password'], data['groups'])
    return res({
        'user': response
    })


@app.route('/deluser', methods=['POST'])
def deluser():
    data = request.get_json()
    response = api.actions.users.delete(data['name'])
    return res()


@app.route('/userlock', methods=['POST'])
def userlock():
    data = request.get_json()
    response = api.actions.users.lock(data['name'])
    return res({'user': response})


@app.route('/userunlock', methods=['POST'])
def userunlock():
    data = request.get_json()
    response = api.actions.users.unlock(data['name'])
    return res({'user': response})


@app.route('/addtogroups', methods=['POST'])
def addtogroups():
    data = request.get_json()
    response = api.actions.users.add_to_groups(data['name'], data['groups'])
    return res({
        'user': response
    })


@app.route('/removefromgroups', methods=['POST'])
def removefromgroups():
    data = request.get_json()
    response = api.actions.users.remove_from_groups(
        data['name'], data['groups'])
    return res({
        'user': response
    })

# group probes and actions
@app.route('/groups')
def groups():
    return res({'groups': api.parsers.groups.parse()})


@app.route('/group/<gid>')
def group(gid):
    return res({'group': api.parsers.groups.parse_single(gid)})


@app.route('/groupadd', methods=['POST'])
def groupadd():
    data = request.get_json()
    response = api.actions.groups.create(data['name'])
    return res({
        'group': response
    })


@app.route('/delgroup', methods=['POST'])
def delgroup():
    data = request.get_json()
    api.actions.groups.delete(data['name'])
    return res()


# misc probes
@app.route('/cpu')
def cpu():
    return res({'cpu': api.parsers.misc.cpu()})


@app.route('/uptime')
def uptime():
    return res({'uptime': api.parsers.misc.uptime()})


@app.route('/hostname')
def hostname():
    return res({'hostname': api.parsers.misc.hostname()})


@app.route('/kernel')
def kernel():
    return res({'kernel': api.parsers.misc.kernel()})


@app.route('/shells')
def shells():
    return res({'shells': api.parsers.misc.shells()})


@app.route('/ssh')
def ssh():
    return res({'ssh': api.parsers.misc.ssh()})


@app.route('/block')
def block():
    return res({'block': api.parsers.misc.block()})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444, debug=True)
