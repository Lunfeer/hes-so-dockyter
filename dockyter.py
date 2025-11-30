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


#Sources (in order)
""" 
https://stackoverflow.com/questions/89228/how-do-i-execute-a-program-or-call-a-system-command
https://docs.python.org/3/library/subprocess.html
https://stackoverflow.com/questions/1924469/define-a-list-with-type
https://ipython.readthedocs.io/en/latest/config/custommagics.html
https://chatgpt.com/share/69273517-bf78-8005-bbce-426ef88687b3
https://stackoverflow.com/questions/41171791/how-to-suppress-or-capture-the-output-of-subprocess-run
https://stackoverflow.com/questions/3022013/windows-cant-find-the-file-on-subprocess-call
https://www.datacamp.com/tutorial/python-concatenate-strings?utm_cid=19589720821&utm_aid=157156375191&utm_campaign=230119_1-ps-other~dsa~tofu_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=9188645-&utm_mtd=-c&utm_kw=&utm_source=google&utm_medium=paid_search&utm_content=ps-other~emea-en~dsa~tofu~tutorial~python&gad_source=1&gad_campaignid=19589720821&gbraid=0AAAAADQ9WsEbLbhJkXNJ16oUoPbjY7Iy-&gclid=CjwKCAiA55rJBhByEiwAFkY1QFGEDvZTU8aJr22JYA5sx1TkzCDCTUtKmLSFskohKJnaPFvwYNQIPxoCrysQAvD_BwE
https://chatgpt.com/share/69275355-5748-8008-8102-c2e34857ef96
 """

if __name__ == '__main__':
    print("Dockyter main")
    line = "ubuntu:latest"
    cmd = "cd home && mkdir Simon && ls"
    print(cmd)
    full_cmd = f'{DOCKER_CALL} {line} {DOCKER_BASH_CALL} "{cmd}"'
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
