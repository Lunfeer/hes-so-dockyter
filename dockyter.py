import subprocess
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.core.getipython import get_ipython

DOCKER_CALL = "docker run --rm"
DOCKER_BASH_CALL = "bash -lc"

@magics_class
class Dockyter(Magics):
    def __init__(self, shell=None, **kwargs):
        super().__init__(shell=shell, **kwargs)
        self.docker_args: str = ""
        self.original_system = None

    def docker_command(self, cmd):
        full_cmd = f'{DOCKER_CALL} {self.docker_args} {DOCKER_BASH_CALL} "{cmd}"'
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout

    def docker_console(self, cmd):
        print(self.docker_command(cmd))

    @line_magic("docker")
    def docker_line(self, line):
        self.docker_args = line

        ip = get_ipython()
        self.original_system = ip.system
        self.docker_on()

        print(self.docker_command("echo 'Connected'"))

    @line_magic("docker_on")
    def docker_on(self, line = ""):
        ip = get_ipython()
        ip.system = self.docker_console
    
    @line_magic("docker_off")
    def docker_off(self, line = ""):
        ip = get_ipython()
        ip.system = self.original_system

    @cell_magic("docker")
    def docker_cell(self, line, cell):
        self.docker_args = line
        commands = " && ".join(cell.splitlines())
        print(self.docker_command(commands))

def load_ipython_extension(ip):
    ip.register_magics(Dockyter)

if __name__ == '__main__':
    print("Dockyter main")
    line = "ubuntu:latest"
    cmd = "cd home && mkdir Simon && ls"
    print(cmd)
    full_cmd = f'{DOCKER_CALL} {line} {DOCKER_BASH_CALL} "{cmd}"'
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
