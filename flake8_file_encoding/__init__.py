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

    @staticmethod
    def get_arg(node, position, keyword):
        """
        Gets an argument from a Call node, where the argument can be specified
        with either a position or a keyword.
        """
        args = node.args
        if len(args) >= position + 1:
            try:
                return args[position].s
            except AttributeError:
                raise TypeError("Argument in position {} is not a string".format(position))
        for kwarg in node.keywords:
            if kwarg.arg == keyword:
                try:
                    return kwarg.value.s
                except AttributeError:
                    raise TypeError('Keyword argument "{}" is not a string'.format(keyword))
        raise ValueError(
            'No argument with position {} or keyword "{}" in node {}'.format(
                position, keyword, repr(node)
            )
        )

    def rule_FEN001(self, node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "open"
        ):
            try:
                mode = self.get_arg(node, 1, "mode")
            except ValueError:
                mode = "r"
            except TypeError:
                # TODO: new error code for invalid modes
                return
            if "b" in mode:
                return

            try:
                self.get_arg(node, 3, "encoding")
            except ValueError:
                yield (
                    node.lineno,
                    node.col_offset,
                    "FEN001 open() call has no encoding argument",
                    type(self),
                )
            except TypeError:
                pass
