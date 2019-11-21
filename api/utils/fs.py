import os


def read_lines(fname):
    if os.path.isfile(fname):
        with open(fname) as file:
            data = file.read()
            lines = filter(None, data.split('\n'))
            return lines
    else:
        raise RuntimeError('\'{}\': no such file'.format(fname))


def read(fname):
    if os.path.isfile(fname):
        return open(fname).read()
    else:
        raise RuntimeError('\'{}\': no such file'.format(fname))
