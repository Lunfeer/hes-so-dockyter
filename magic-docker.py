from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)

@magics_class
class MyMagics(Magics):
    @line_magic("test")
    def hello(self, line):
        print(f"Hello: {line}")

    @cell_magic("test")
    def echo(self, line, cell):
        print(f"Line: {line}")
        print(cell)

def load_ipython_extension(ip):
    ip.register_magics(MyMagics)