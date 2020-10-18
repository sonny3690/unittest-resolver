import ast
from contextlib import contextmanager
from types import ModuleType
from typing import List
import test
import inspect
from collections import defaultdict


class Context(dict):
    ...


class Reader:
    @staticmethod
    @contextmanager
    def read(testModuleName: str):
        pass

    def _findPathModule(self, path: str):
        pass


def _extractFunctionCalls(node: ast):
    pass


def recurse(parent: ast, num=0):
    print('level ------ {}'.format(num))
    for node in ast.iter_child_nodes(parent):
        print('node', node)
        print(ast.dump(node))

        if hasattr(node, 'id'):
            print(node.id)
        recurse(node, num+1)


def findUnitTestClass(classNode: ast.ClassDef):
    def _isUnitTest(base: List[ast.expr]) -> bool:
        return base.value.id == 'unittest' and base.attr == 'TestCase'

    if not any(map(_isUnitTest, classNode.bases)):
        return False

    recurse(node)


def hi():
    pass


with open("test.py", "r") as source:
    tree = ast.parse(source.read())

for node in ast.iter_child_nodes(tree):
    if isinstance(node, ast.ClassDef):
        findUnitTestClass(node)
