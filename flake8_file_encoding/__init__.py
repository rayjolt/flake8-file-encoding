"""
This is a Flake8 plugin to check for missing "encoding" arguments.

For documentation, see <https://github.com/rayjolt/flake8-file-encoding>.
"""

import ast
import collections
from enum import Enum

import pkg_resources

__version__ = pkg_resources.get_distribution("flake8-file-encoding").version


Argument = collections.namedtuple("Argument", ["state", "value"])


class ArgumentState(Enum):
    """An enum representing the state of an argument to a callable."""

    POSITIONAL = 1
    KEYWORD = 2
    NOTFOUND = 3


class EncodingChecker:
    """A Flake8 checker to check for missing "encoding" arguments.

    Parameters
    ----------
    tree
        The abstract syntax tree of the source file being checked.

    """

    name = __name__
    version = __version__

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        """Run all checks."""
        for node in ast.walk(self.tree):
            for err in self.rule_FEN001(node):
                yield err

    @staticmethod
    def _get_arg(node, position, keyword):
        """Get an argument from an AST Call node."""
        args = node.args
        if len(args) >= position + 1:
            return Argument(ArgumentState.POSITIONAL, args[position])
        for kwarg in node.keywords:
            if kwarg.arg == keyword:
                return Argument(ArgumentState.KEYWORD, kwarg)
        return Argument(ArgumentState.NOTFOUND, None)

    def rule_FEN001(self, node):
        """Check open() calls have an "encoding" argument."""
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "open"
        ):
            mode = self._get_arg(node, 1, "mode")
            if mode.state == ArgumentState.NOTFOUND:
                mode = "r"
            elif isinstance(mode.value, ast.Str):
                mode = mode.value.s
            else:
                # TODO: new error code for invalid modes
                return
            if "b" in mode:
                return

            encoding = self._get_arg(node, 3, "encoding")
            if encoding.state == ArgumentState.NOTFOUND:
                yield (
                    node.lineno,
                    node.col_offset,
                    "FEN001 open() call has no encoding argument",
                    type(self),
                )
