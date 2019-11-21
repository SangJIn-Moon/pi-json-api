import subprocess
import re
import api.utils.fs


def _exists_lines(lines, username):
    if any(username in s for s in lines):
        return True
    return False


def exists(username):
    # both username or user id
    lines = api.utils.fs.read_lines('/etc/passwd')
    return _exists_lines(lines, username)


def _is_builtin_uid_name(uid, name):
    # make sure uid is an int!
    if int(uid) > 999:
        if name != 'nobody':
            return False
    return True


def _is_builtin_lines(lines, username):
    index = [i for i, s in enumerate(lines) if username in s]
    line = lines[index]
    col = line.split(':')
    _is_builtin_uid_name(int(col[2]), col[0])
    return True


def is_builtin(username):
    # both username or user id
    lines = api.utils.fs.read_lines('/etc/passwd')
    # check if user exists
    if _exists_lines(lines, username):
        return _is_builtin_lines(lines, username)
    return True


def parse():
    lines = api.utils.fs.read_lines('/etc/passwd')
    proc = subprocess.Popen(
        ('sudo cat /etc/shadow').split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    shadow_lines = filter(None, stdout.split('\n'))
    out = []
    for line in lines:
        col = line.split(':')
        is_builtin = _is_builtin_uid_name(int(col[2]), col[0])
        # this allows us to do one read through cat (better than N reads)
        locked = _is_locked_lines(shadow_lines, col[0])
        obj = {
            'name': col[0],
            'uid': int(col[2]),
            'gid': int(col[3]),
            'home': col[5],
            'shell': col[6],
            'builtin': is_builtin,
            'is_locked': locked
        }
        out.append(obj)
    return out


def _get_groups_stdout(stdout, username):
    matches = re.findall(r'(\d+)\((\w+|\d+)\)', stdout)
    matches = matches[2:]
    out = []
    for group in matches:
        out.append({
            'gid': int(group[0]),
            'name': group[1]
        })
    return out


def get_groups(username):
    proc = subprocess.Popen(
        ("id -a {}".format(username)).split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    return _get_groups_stdout(stdout, username)


def _is_locked_lines(lines, username):
    for line in lines:
        if line.startswith('{}:'.format(username)):
            col = line.split(':')
            if '!' in col[1]:
                return True
            return False


def is_locked(username):
    # NOTE: only the name is a valid parameter, not the UID!!
    proc = subprocess.Popen(
        ('sudo cat /etc/shadow').split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    shadow_lines = filter(None, stdout.split('\n'))
    return _is_locked_lines(shadow_lines, username)


def parse_single(username):
    proc = subprocess.Popen(
        ("id -a {}".format(username)).split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    matches = re.findall(r'(\d+)\((\w+|\d+)\)', stdout)
    if not matches:
        raise RuntimeError('\'{}\': no such user'.format(username))
    is_builtin = _is_builtin_uid_name(int(matches[0][0]), matches[0][1])
    # check if user is locked
    locked = is_locked(matches[0][1])
    out = {
        'name': matches[0][1],
        'uid': matches[0][0],
        'is_builtin': is_builtin,
        'is_locked': locked
    }
    groups = _get_groups_stdout(stdout, username)
    out['groups'] = groups
    return out
