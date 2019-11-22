import api.parsers.groups
from api.utils.cmd import shell
import api.parsers.groups


def create(name):
    shell('sudo groupadd {}'.format(name))
    return api.parsers.groups.parse_single(name)


def delete(name):
    shell('sudo groupdel {}'.format(name))
    if api.parsers.groups.exists(name):
        return False
    return True
