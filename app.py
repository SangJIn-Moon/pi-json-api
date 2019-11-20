import subprocess
import re
import os
from flask import Flask
from flask import request

app = Flask(__name__)

version = '0.1.0'

dirname = os.path.dirname(os.path.realpath(__file__))


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


@app.route('/users')
def users():
    proc = subprocess.Popen("cat /etc/passwd".split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()

    list = []

    lines = filter(None, out.split('\n'))
    for line in lines:
        col = line.split(':')

        # info = None
        # if col[4]:
        #     user_info = col[4].split(',')
        #     if len(user_info) > 1:
        #         info = {
        #             'full_name': user_info[0] if user_info[0] != '' else None,
        #             'room_number': user_info[1] if user_info[1] != '' else None,
        #             'work_phone': user_info[2] if user_info[2] != '' else None,
        #             'home_phone': user_info[3] if user_info[3] != '' else None,
        #         }

        user_object = {
            'name': col[0],
            # 'password': col[1],
            'uid': int(col[2]),
            'gid': int(col[3]),
            # 'info': info,
            'home': col[5],
            'shell': col[6]
        }
        list.append(user_object)
    return res({
        'version': version,
        'users': list
    })


@app.route('/user/<username>')
def user(username):
    proc = subprocess.Popen(
        ("id -a {}".format(username)).split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    # format
    # uid=<int>(<string>) gid=<int>(<string>) groups=[<int>(<string>),]
    matches = re.findall(r'(\d+)\((\w+|\d+)\)', out)
    if not matches:
        return {
            'version': version,
            'error': '\'{}\': no such user'.format(username)
        }
    groups_list = []
    gm = matches[2:]
    for g in gm:
        groups_list.append({
            'gid': int(g[0]),
            'name': g[1]
        })
    return res({
        'version': version,
        'user': {
            'name': matches[0][1],
            'uid': int(matches[0][0]),
            'groups': groups_list
        }
    })


@app.route('/group/<name>')
def group(name):
    proc = subprocess.Popen(
        ("getent group {}".format(name)).split(), stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if not out:
        return {
            'version': version,
            'error': '\'{}\': no such group'.format(name)
        }
    # parse group name and id
    parts = filter(None, out.split(':'))
    members = []
    proc = subprocess.Popen(
        ("members {}".format(parts[0])).split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    members = filter(None, out.split())
    return res({
        'version': version,
        'group': {
            'name': parts[0],
            'gid': int(parts[2]),
            'members': members
        }
    })


@app.route('/groups')
def groups():
    """
    NOTE:   this command requires `members'
            sudo apt-get install members
    """
    proc = subprocess.Popen("cat /etc/group".split(), stdout=subprocess.PIPE)
    out, err = proc.communicate()

    list = []
    lines = filter(None, out.split('\n'))
    for line in lines:
        col = filter(None, line.split(':'))
        # get members
        members = []
        proc = subprocess.Popen(("members {}".format(
            col[0])).split(), stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = filter(None, out.split('\n'))
        if len(out) > 0:
            members = filter(None, out[0].split())
        group_object = {
            'name': col[0],
            # 'password': col[1],
            'gid': int(col[2]),
            'members': members
        }
        list.append(group_object)
    return res({
        'version': version,
        'groups': list
    })


@app.route('/net')
def interfaces():
    proc = subprocess.Popen("netstat -i".split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    lines = filter(None, out.split('\n'))
    # remove headers
    lines = lines[2:]
    list = []
    for line in lines:
        col = line.split()
        iface_object = {
            'name': col[0],
        }
        list.append(iface_object)

    return res({
        'version': version,
        'interfaces': list
    })


@app.route('/disk')
def disk():
    command = 'df -B1 --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs'
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    lines = filter(None, out.split('\n'))
    # remove headers
    lines = lines[1:]
    list = []
    for line in lines:
        col = line.split()
        fs_object = {
            'filesystem': col[0],
            'type': col[1],
            'size': int(col[2]),
            'used': int(col[3]),
            'available': int(col[4]),
            'percent': int(re.sub('%$', '', col[5])),
            'mount_point': col[6]
        }
        list.append(fs_object)
    return res({
        'version': version,
        'disk': list
    })


@app.route('/adduser', methods=['POST'])
def adduser():
    # TODO(everdrone): check that username is eligible and it doesn't exist yet
    data = request.get_json()
    proc = subprocess.Popen(
        './adduser.sh'.split(),
        cwd=os.path.join(dirname, 'scripts'),
        env=dict(
            os.environ,
            username=data['name'],
            groups=','.join(data['groups']),
            password=data['password']
        ),
        stdout=subprocess.PIPE
    )
    out, _ = proc.communicate()

    return res({
        'version': version,
        'user': {
            'name': data['name'],
            'groups': data['groups']
        }
    })


@app.route('/deluser', methods=['DELETE'])
def deluser():
    # TODO(everdrone): check if user has a uid > 999 (not builtin user)
    data = request.get_json()
    proc = subprocess.Popen(
        'sudo deluser {} {}'.format(
            '--remove-home' if data['remove_home'] else '',
            data['name']
        ).split(),
        stdout=subprocess.PIPE
    )
    out, _ = proc.communicate()

    # TODO(everdrone): check that user doesn't exist anymore in /etc/passwd
    return res({
        'version': version,
        'user': data['name']
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444, debug=True)
