import subprocess
import re
from flask import Flask

app = Flask(__name__)

version = '0.1.0'


@app.route('/')
def index():
    return {
        'version': version,
    }


@app.route('/users')
def users():
    proc = subprocess.Popen("cat /etc/passwd".split(), stdout=subprocess.PIPE)
    out, _ = proc.communicate()

    list = []

    lines = filter(None, out.split('\n'))
    for line in lines:
        col = line.split(':')
        """
        info = None
        if col[4]:
            user_info = col[4].split(',')
            if len(user_info) > 1:
                info = {
                    'full_name': user_info[0] if user_info[0] != '' else None,
                    'room_number': user_info[1] if user_info[1] != '' else None,
                    'work_phone': user_info[2] if user_info[2] != '' else None,
                    'home_phone': user_info[3] if user_info[3] != '' else None,
                }
        """
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
    return {
        'version': version,
        'users': list
    }


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
    return {
        'version': version,
        'groups': list
    }


@app.route('/interfaces')
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

    return {
        'version': version,
        'interfaces': list
    }


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
    return {
        'version': version,
        'disk': list
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444, debug=True)
