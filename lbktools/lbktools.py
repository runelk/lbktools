
from commands import mtag, cg3, stat, dep
import subprocess

def run_command(cmd, s):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return p.communicate(s)

def run_mtag(s):
    return run_command(mtag, s)

def run_cg3(s):
    return run_command(cg3, s)

def run_stat(s):
    return run_command(stat, s)

def run_dep():
    print dep
