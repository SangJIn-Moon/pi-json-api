def read_lines(fname):
    with open(fname) as file:
        data = file.read()
        lines = filter(None, data.split('\n'))
        return lines
