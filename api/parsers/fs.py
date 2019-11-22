import re
import os
import stat
import api.utils.fs
import api.utils.fs
from api.utils.cmd import shell


def _find_device(device):
    for dirname in ['/dev', '/dev/mapper']:
        path = os.path.join(dirname, device)
        mode = os.stat(path).st_mode
        is_blk = stat.S_ISBLK(mode)
        if is_blk:
            return path


def _update_missing(out, obj):
    keys_to_update = []
    for key in out.keys():
        if key.startswith(obj['dev']):
            keys_to_update.append(key)

    if not len(keys_to_update):
        key = '{},'.format(obj['dev'])
        out[key] = {}
        out[key]['device'] = obj['dev']
        keys_to_update.append(key)

    for kk in keys_to_update:
        for subkey in ['fs_type', 'uuid', 'label']:
            if obj.get(subkey) and not bool(obj.get(subkey)):
                out[kk][subkey] = obj[subkey]
    return out


def filesystem():
    out = {}
    lines = shell('df -P')
    lines = filter(None, lines.split('\n'))
    df_p = {}
    for line in lines:
        match = re.match(
            '^(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\%)\s+(.+)$', line)
        if match:
            mg = match.groups()
            key = '{},{}'.format(mg[0], mg[5])
            df_p[key] = {}
            df_p[key]['device'] = mg[0]
            df_p[key]['kb_size'] = mg[1]
            df_p[key]['kb_used'] = mg[2]
            df_p[key]['kb_available'] = mg[3]
            df_p[key]['percent_used'] = mg[4]
            df_p[key]['mount'] = mg[5]
    # merge into out object
    out.update(df_p)

    # filesystem inode data
    lines = shell('df -iP')
    lines = filter(None, lines.split('\n'))
    df_ip = {}
    for line in lines:
        match = re.match(
            '^(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\%)\s+(.+)$', line)
        if match:
            mg = match.groups()
            key = '{},{}'.format(mg[0], mg[5])
            df_ip[key] = {}
            df_ip[key]['device'] = mg[0]
            df_ip[key]['total_inodes'] = mg[1]
            df_ip[key]['inodes_used'] = mg[2]
            df_ip[key]['inodes_available'] = mg[3]
            df_ip[key]['inodes_percent_used'] = mg[4]
            df_ip[key]['mount'] = mg[5]
    # merge into out obj
    out.update(df_ip)

    # grab mount data
    lines = shell('mount')
    lines = filter(None, lines.split('\n'))
    mount = {}
    for line in lines:
        match = re.match('^(.+?) on (.+?) type (.+?) \((.+?)\)$', line)
        if match:
            mg = match.groups()
            key = '{},{}'.format(mg[0], mg[1])
            mount[key] = {}
            mount[key]['device'] = mg[0]
            mount[key]['mount'] = mg[1]
            mount[key]['fs_type'] = mg[2]
            mount[key]['mount_options'] = mg[3].split(',')
    # merge into out
    out.update(mount)

    # grab from /proc/mounts
    lines = api.utils.fs.read_lines('/proc/mounts')
    # don't merge directly into out
    # check if the data is missing, if it is, then merge
    proc = {}
    for line in lines:
        match = re.match('^(\S+) (\S+) (\S+) (\S+) \S+ \S+$', line)
        if match:
            mg = match.groups()
            key = '{},{}'.format(mg[0], mg[1])
            proc[key] = {}
            proc[key]['device'] = mg[0]
            proc[key]['mount'] = mg[1]
            proc[key]['fs_type'] = mg[2]
            proc[key]['mount_options'] = mg[3].split(',')
            # update only if missing
            if key not in out.keys():
                out[key] = proc[key]

    # grab lsblk data
    lines = shell('lsblk -n -P -o NAME,UUID,LABEL,FSTYPE')
    lines = filter(None, lines.split('\n'))
    lsblk = []
    for line in lines:
        match = re.match(
            'NAME="(\S+).*?" UUID="(\S*)" LABEL="(\S*)" FSTYPE="(\S*)"', line)
        if match:
            mg = match.groups()
            dev = mg[0]
            if not dev.startswith('/'):
                dev = _find_device(dev)
            uuid = mg[1]
            label = mg[2]
            fs_type = mg[3]
            obj = {
                'dev': dev,
                'uuid': uuid,
                'label': label,
                'fs_type': fs_type
            }
            lsblk.append(obj)
            # update
            out = _update_missing(out, obj)

    # grab blkid data
    lines = shell('blkid')
    lines = filter(None, lines.split('\n'))
    blkid = []
    for line in lines:
        device_name = line.split(':')[0]
        obj = {
            'dev': device_name
        }
        parts = line.split()[1:]
        for part in parts:
            match = re.match('(\S+)="(\S+)"', part)
            if match:
                mg = match.groups()
                key = mg[0].lower()
                if key == 'type':
                    key = 'fs_type'
                obj[key] = mg[1]
        # update
        out = _update_missing(out, obj)

    return out


def parse(mode):
    fs = filesystem()
    if 'pair':
        return fs
    if 'device':
        out = {}
        for entry in out.keys():
            out[entry['device']] = {}
            for key, val in entry.item():
                if not (key == 'mount' or key == 'device'):
                    out[entry['device']][key] = val
            out[entry['device']]['mounts'] = []
            if entry['mount']:
                out[entry['device']]['mounts'].append(entry['mount'])
        return out
    if 'mountpoint':
        pass
    else:
        pass
