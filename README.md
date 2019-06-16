# flake8-file-encoding

A Flake8 plugin to check for files opened without an explicit encoding.

## Why check for encoding arguments?

If you don't specify an `encoding` argument to the
[open](https://docs.python.org/3/library/functions.html#open) function, then
Python will use a platform-dependent default encoding—whatever
[locale.getpreferredencoding](https://docs.python.org/3/library/locale.html#locale.getpreferredencoding)
returns. On many platforms this is
[UTF-8](https://en.wikipedia.org/wiki/UTF-8), but on a significant minority it
is something different. For example, the default encoding on Japanese Windows
machines is cp932 (Microsoft's version of
[Shift-JIS](https://en.wikipedia.org/wiki/Shift_JIS)). If you open a UTF-8 file
on such a system but do not specify an encoding, then attempting to read any
multi-byte characters in the file will cause a UnicodeDecodeError.

## Installation

```bash
pip install flake8-file-encoding
```

## Usage

Once this plugin is installed, Flake8 will check for missing `encoding`
arguments along with its other checks. No special activation for this plugin is
necessary. For more details on running Flake8, see the
[Flake8 documentation](http://flake8.pycqa.org/en/latest/index.html).

## Errors

Code   | Message
------ | --------
FEN001 | open() call has no encoding argument
