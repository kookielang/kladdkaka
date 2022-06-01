"""
Kladdkaka REPL
"""
import os

import colorama
from colorama import Fore

from .codeanalysis.evaluator import Evaluator
from .codeanalysis.syntaxnode import SyntaxNode
from .codeanalysis.syntaxtoken import SyntaxToken
from .codeanalysis.syntaxtree import SyntaxTree

colorama.init(autoreset=True)
SHOWTREE = False


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True) -> None:
    """
    Print the syntaxtokens as a tree.
    """
    marker = '└──' if is_last else '├──'

    print(indent, end="")
    print(marker, end="")
    print(node.kind.name, end="")

    if isinstance(node, SyntaxToken):
        if node.value is not None:
            print(" ", end="")
            print(node.value, end="")

    print()

    indent += '   ' if is_last else '│   '

    try:
        last_child = node.get_children()[-1]
    except IndexError:
        last_child = None

    for child in node.get_children():
        pretty_print(child, indent, last_child == child)


while True:
    line = input("» ")
    # › ⊸ ⋯

    if line is None or line == "":
        break

    if line == "#showtree":
        SHOWTREE = not SHOWTREE
        print("Showing parser trees" if SHOWTREE else "Not showing parser trees")
        continue
    if line == "#cls":
        os.system('cls')
        continue

    syntax_tree = SyntaxTree.parse(line)

    if SHOWTREE:
        pretty_print(syntax_tree.root)

    if not len(syntax_tree.diagnostics) > 0:
        evaluator = Evaluator(syntax_tree.root)
        result = evaluator.evaluate()
        print(str(result))
    else:
        for _diagnostic in syntax_tree.diagnostics:
            print(Fore.RED + _diagnostic)
