import os
import subprocess

def shell(command, cwd=None, env={}):
    environ = os.environ.copy()
    environ.update(env)
    proc = subprocess.Popen(
        command.split(),
        cwd = cwd,
        env = environ,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    if stderr:
        raise RuntimeError(
            'command {} exited with non zero:\n{}'.format(command, stderr))
    return stdout
