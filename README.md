# dont

don't: use this!

## Usage

```python
import dont

with dont():
    1/0  # this will not cause an exception
```

More interestingly, you can subclass `dont` to do any kind of custom behaviour
with the contents of the context manager:

```python
class bash(dont):
    def hook(self):
        for line in self.content:
            os.system(line.replace("%", " "))

with bash():   # prints "hello" and touches the file `me`:
    echo % hello
    touch % me
```

The most annoying restriction here is that the contents of the context manager
still have to be syntactically valid Python.

## Ideas

What could you do with this?

- `remotely(some_host)` — execute a python code block on a remote host,
  fabric-style?
- `production` — only execute code when we're on a production server
- `reverse` — execute lines in inverted order
