import re
import humanfriendly
import api.utils.fs
import api.utils.misc


def _parse_memory_size_pair(size, unit):
    return humanfriendly.parse_size('{} {}'.format(size, unit))


def parse():
    lines = api.utils.fs.read_lines('/proc/meminfo')
    out = {}
    # todo: parse size into kbytes or bytes
    for line in lines:
        match = re.match('^MemTotal:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^MemFree:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['free'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^MemAvailable:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['available'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Buffers:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['buffers'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Cached:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['cached'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Active:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['active'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Inactive:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['inactive'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^HighTotal:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('high', out)
            mg = match.groups()
            out['high']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^HighFree:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('high', out)
            mg = match.groups()
            out['high']['free'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^LowTotal:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('low', out)
            mg = match.groups()
            out['low']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^LowFree:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('low', out)
            mg = match.groups()
            out['low']['free'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Dirty:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['dirty'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Writeback:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['writeback'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^AnonPages:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['anon_pages'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Mapped:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['mapped'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Slab:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('slab', out)
            mg = match.groups()
            out['slab']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^SReclaimable:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('slab', out)
            mg = match.groups()
            out['slab']['reclaimable'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^SUnreclaim:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('slab', out)
            mg = match.groups()
            out['slab']['unreclaim'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^PageTables:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['page_tables'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^NFS_Unstable:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['nfs_unstable'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Bounce:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['bounce'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^CommitLimit:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['commit_limit'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Committed_AS:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['committed_as'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^VmallocTotal:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('vmalloc', out)
            mg = match.groups()
            out['vmalloc']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^VmallocUsed:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('vmalloc', out)
            mg = match.groups()
            out['vmalloc']['used'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^VmallocChunc:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('vmalloc', out)
            mg = match.groups()
            out['vmalloc']['chunk'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^SwapCached:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('swap', out)
            mg = match.groups()
            out['swap']['cached'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^SwapTotal:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('swap', out)
            mg = match.groups()
            out['swap']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^SwapFree:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('swap', out)
            mg = match.groups()
            out['swap']['free'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^HugePages_Total:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('hugepages', out)
            mg = match.groups()
            out['hugepages']['total'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^HugePages_Free:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('hugepages', out)
            mg = match.groups()
            out['hugepages']['free'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^HugePages_Rsvd:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('hugepages', out)
            mg = match.groups()
            out['hugepages']['reserved'] = _parse_memory_size_pair(
                mg[0], mg[1])
        match = re.match('^HugePages_Surp:\s+(\d+) (.+)$', line)
        if match:
            api.utils.misc.cond_init_key('hugepages', out)
            mg = match.groups()
            out['hugepages']['surplus'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^Hugepagesize:\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['hugepage_size'] = _parse_memory_size_pair(mg[0], mg[1])
        match = re.match('^DirectMap([0-9]+[a-zA-Z]):\s+(\d+) (.+)$', line)
        if match:
            mg = match.groups()
            out['directmap'] = {}
            out['directmap'][mg[0]] = _parse_memory_size_pair(mg[1], mg[2])
    return out
