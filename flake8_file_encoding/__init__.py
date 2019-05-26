import ast

__version__ = "0.1.0"


class EncodingChecker:
    name = __name__
    version = __version__

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            for err in self.rule_FEN001(node):
                yield err

    def rule_FEN001(self, node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "open"
        ):
            for kwarg in node.keywords:
                if kwarg.arg == "encoding":
                    break
            else:
                yield (
                    node.lineno,
                    node.col_offset,
                    "FEN001 open() called without an encoding argument",
                    type(self),
                )
