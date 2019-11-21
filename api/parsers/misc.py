import subprocess
import re
import os
import api.utils.fs


def cpu():
    lines = api.utils.fs.read_lines('/proc/cpuinfo')
    out = {
        'processors': []
    }
    cpu_number = -1
    for line in lines:
        match = re.match('processor\s+:\s(.+)', line)
        if match:
            cpu_number += 1
            out['processors'].append({})
            out['processors'][cpu_number]['processor'] = int(match.group(1))
        match = re.match('model\sname\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['model_name'] = match.group(1)
        match = re.match('BogoMIPS\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['bogo_mips'] = float(match.group(1))
        match = re.match('Features\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['features'] = match.group(1).split()
        match = re.match('CPU\simplementer\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['cpu_implementer'] = match.group(1)
        match = re.match('CPU\sarchitecture\s*:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['cpu_architecture'] = int(
                match.group(1))
        match = re.match('CPU\svariant\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['cpu_variant'] = match.group(1)
        match = re.match('CPU\spart\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['cpu_part'] = match.group(1)
        match = re.match('CPU\srevision\s+:\s(.+)', line)
        if match:
            out['processors'][cpu_number]['cpu_revision'] = int(match.group(1))
        match = re.match('Hardware\s+:\s(.+)', line)
        if match:
            out['hardware'] = match.group(1)
        match = re.match('Revision\s+:\s(.+)', line)
        if match:
            out['revision'] = match.group(1)
        match = re.match('Serial\s+:\s(.+)', line)
        if match:
            out['serial'] = match.group(1)
        match = re.match('Model\s+:\s(.+)', line)
        if match:
            out['model'] = match.group(1)
    return out


def uptime():
    # todo use open().read()
    uptime, idletime = api.utils.fs.read_lines('/proc/uptime')[0].split()
    return {
        'uptime': int(round(float(uptime))),
        'idletime': int(round(float(idletime))),
    }


def hostname():
    # domain name
    proc = subprocess.Popen(
        ("hostname -f").split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    fqdn = stdout.strip()
    # ip address
    proc = subprocess.Popen(
        ("hostname -I").split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    ip_addr = stdout.strip()
    return {
        'fqdn': fqdn,
        'ip': ip_addr
    }


def kernel():
    toup = [
        ['name', 'uname -s'],
        ['processor', 'uname -p'],
        ['release', 'uname -r'],
        ['version', 'uname -v'],
        ['machine', 'uname -m'],
    ]

    out = {}

    for cmd in toup:
        proc = subprocess.Popen((cmd[1]).split(), stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
        str = stdout.strip()
        out[cmd[0]] = str

    proc = subprocess.Popen("env lsmod".split(), stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    lines = filter(None, stdout.split('\n'))
    lsmod = {}
    for module in lines:
        match = re.match('([a-zA-Z0-9\_]+)\s+(\d+)\s+(\d+)', module)
        if match:
            name = match.groups(1)[0]
            lsmod[name] = {
                'size': match.groups(1)[1],
                'refcount': match.groups(1)[1]
            }
            # get module version
            path = '/sys/module/{}/version'.format(name)
            if os.path.isfile(path):
                version = open(path).read().strip()
                if version:
                    lsmod[name]['version'] = version
    out['modules'] = lsmod
    return out


def shells():
    lines = api.utils.fs.read_lines('/etc/shells')
    out = []
    for line in lines:
        if line.startswith('/'):
            out.append(line.strip())
    return out


def ssh():
    out = {}
    try:
        dsa = api.utils.fs.read('/etc/ssh/ssh_host_dsa_key.pub')
        out['host_dsa_public'] = dsa.split()[1]
    except:
        pass
    try:
        rsa = api.utils.fs.read('/etc/ssh/ssh_host_rsa_key.pub')
        out['host_rsa_public'] = rsa.split()[1]
    except:
        pass
    try:
        ecdsa = api.utils.fs.read('/etc/ssh/ssh_host_ecdsa_key.pub')
        out['host_ecdsa_public'] = ecdsa.split()[1]
        out['host_ecdsa_type'] = ecdsa.split()[0]
    except:
        pass
    try:
        ed25519 = api.utils.fs.read('/etc/ssh/ssh_host_ed25519_key.pub')
        out['host_ed25519_public'] = ed25519.split()[1]
    except:
        pass
    return out


def block():
    list = os.listdir('/sys/block')
    out = {}
    for block in list:
        out[block] = {}
        for check in ['size', 'removable']:
            try:
                data = api.utils.fs.read(
                    '/sys/block/{}/{}'.format(block, check))
                if check == 'removable':
                    out[block][check] = bool(data.strip())
                else:
                    out[block][check] = int(data.strip())
            except:
                pass
        for check in ['model', 'rev', 'state', 'timeout', 'vendor', 'queue_depth']:
            try:
                data = api.utils.fs.read(
                    '/sys/block/{}/device/{}'.format(block, check))
                out[block][check] = data.strip()
            except:
                pass
        for check in ['rotational', 'physical_block_size', 'logical_block_size']:
            try:
                data = api.utils.fs.read(
                    '/sys/block/{}/queue/{}'.format(block, check))
                if check == 'rotational':
                    out[block][check] = bool(data.strip())
                else:
                    out[block][check] = int(data.strip())
            except:
                pass
    return out
