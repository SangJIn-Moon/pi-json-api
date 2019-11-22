import re
import os
import api.parsers.users
from api.utils.cmd import shell


def lock(username):
    shell('sudo usermod -L {}'.format(username))
    status = shell('sudo passwd -S {}'.format(username))
    if not re.findall('\s(L)\s', status):
        raise RuntimeError('cannot lock user {}'.format(username))
    return api.parsers.users.parse_single(username)


def unlock(username):
    # sudo usermod -U <username>
    #   use sudo passwd --status <username> to check the status of the lock
    #   <username> LK 2019-05-30 7 90 7 -1 (Password locked.)
    shell('sudo usermod -U {}'.format(username))
    status = shell('sudo passwd -S {}'.format(username))
    if re.findall('\s(L)\s', status):
        raise RuntimeError('cannot unlock user {}'.format(username))
    return api.parsers.users.parse_single(username)


def create(username, password=None, groups=[]):
    # TODO(everdrone): make this global
    cwd = '/home/telegram/test/pi-json-api/scripts'
    env = {
        'username': username,
    }
    if password:
        env['password'] = password
    if groups:
        env['groups'] = ','.join(groups)
    print(env)
    shell('bash adduser.sh', cwd, env)
    if api.parsers.users.exists(username):
        return api.parsers.users.parse_single(username)
    return False


def delete(username, remove_home=True):
    if remove_home:
        shell('sudo deluser --remove-home {}'.format(username))
    else:
        shell('sudo deluser {}'.format(username))
    if api.parsers.users.exists(username):
        return False
    return True


def add_to_groups(username, groups):
    groups_string = ','.join(groups)
    shell('sudo usermod -a -G {} {}'.format(groups_string, username))
    should = []
    for ag in api.parsers.users.get_groups(username):
        should.append(ag['name'])
    if all(name in should for name in groups):
        return api.parsers.users.parse_single(username)


def remove_from_groups(username, groups):
    for group in groups:
        shell('sudo gpasswd -d {} {}'.format(username, group))
    should = []
    for ag in api.parsers.users.get_groups(username):
        should.append(ag['name'])
    if not all(name in should for name in groups):
        return api.parsers.users.parse_single(username)
