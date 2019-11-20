import subprocess
import re
import api.utils.fs


def _exists_lines(lines, groupname):
    if any(groupname in s for s in lines):
        return True
    return False


def gid_from_name(name):
    lines = api.utils.fs.read_lines('/etc/group')
    if _exists_lines(lines, name):
        index = [i for i, s in enumerate(lines) if name in s]
        line = lines[index]
        col = line.split(':')
        return int(col[2])
    return False


def name_from_gid(gid):
    lines = api.utils.fs.read_lines('/etc/group')
    if _exists_lines(lines, gid):
        index = [i for i, s in enumerate(lines) if gid in s]
        line = lines[index]
        col = line.split(':')
        return int(col[0])
    return False


def exists(groupname):
    lines = api.utils.fs.read_lines('/etc/group')
    return _exists_lines(lines, groupname)


def get_members(groupname):
    if exists(groupname):
        name = groupname
        if int(groupname):
            # get name from group id
            name = name_from_gid(groupname)

        proc = subprocess.Popen(("members {}".format(
            name)).split(), stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()

        lines = filter(None, stdout.split('\n'))
        members = []
        if len(lines) > 0:
            members = filter(None, lines[0].split())
        return members
    return False


def parse():
    lines = api.utils.fs.read_lines('/etc/group')
    out = []
    for line in lines:
        col = filter(None, line.split(':'))
        group = {
            'name': col[0],
            'gid': int(col[2]),
            'members': get_members(col[0])
        }
        out.append(group)
    return out


def parse_single(groupname):
    proc = subprocess.Popen(
        ("getent group {}".format(groupname)).split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    if not stdout:
        raise RuntimeError('\'{}\': no such group'.format(groupname))
    col = filter(None, stdout.split(':'))
    members = get_members(groupname)
    return {
        'name': col[0],
        'gid': int(col[2]),
        'members': members
    }
