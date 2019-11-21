import subprocess
import re
import os
from flask import Flask
from flask import request

import api.parsers.users
import api.parsers.groups
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

# group probes and actions
@app.route('/groups')
def groups():
    return res({'groups': api.parsers.groups.parse()})


@app.route('/group/<gid>')
def group(gid):
    return res({'group': api.parsers.groups.parse_single(gid)})


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
