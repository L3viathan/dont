import sys
import inspect
import textwrap

def raiser(frame, ttype, arg):
    raise

def indent(line):
    return len(line) - len(line.lstrip(" "))

class dont:
    def __enter__(self):
        self.frame = sys._getframe().f_back
        lines = inspect.getsource(self.frame).split("\n")
        start = self.frame.f_lineno
        start_indent = indent(lines[start])
        stop = next(
            i for i in range(start + 1, len(lines)) if indent(lines[i]) < start_indent
        )
        self.content = textwrap.dedent("\n".join(lines[start:stop])).split("\n")

        sys.settrace(raiser)
        self.frame.f_trace = raiser

    def hook(self):
        pass

    def __exit__(self, *args):
        self.hook()
        return True

sys.modules["dont"] = dont
