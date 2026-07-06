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
##        lines = inspect.getsource(self.frame).split("\n")
        lines, _lnum = inspect.findsource(self.frame) #get the whole file so that .f_lineno still makes sense, even in function, method, or class scope 
        lines = ''.join(lines).split("\n")
        
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

if __name__ == '__main__':#run some tests
    class emit(dont):
        def hook(self):
            print(*self.content, sep='\n')

    with emit():
        "Greetings from global scope"
    def func():
        with emit():
            "Greetings from function scope"
    func()
    
    class cls(object):
        with emit():
            "Greetings from class scope"
        def method(self):
            with emit():
                "Greetings from method scope"
    cls().method()
