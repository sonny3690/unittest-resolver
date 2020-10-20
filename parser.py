import ast
from contextlib import contextmanager
from types import ModuleType
from typing import List
import test
import inspect
from collections import defaultdict, deque
from typeguards import _isClassDef, _isScopeCreator


class Context(dict):

    def __init__(self, parent=None):
        self.__parent = parent

    def _parent(self):
        pass

    _parent: 'Class' = None
    _children: List['Class'] = []


class Reader:
    @staticmethod
    @contextmanager
    def read(testModuleName: str):
        pass

    def _findPathModule(self, path: str):
        pass


def _extractFunctionCalls(node: ast):
    pass


_global_context = Context()


def recurse(parent: ast, *, context: Context = None, num=0) -> None:
    if context is None:
        context = _global_context

    for node in ast.iter_child_nodes(parent):
        if _isScopeCreator(node):
            context = Context()

        if hasattr(node, 'id'):
            print(node.id)
        recurse(node, context=context, num=num+1)


def findUnitTestClass(classNode: ast.ClassDef):
    def _isUnitTest(base: List[ast.expr]) -> bool:
        return base.value.id == 'unittest' and base.attr == 'TestCase'

    if not any(map(_isUnitTest, classNode.bases)):
        return False
    recurse(node)


with open("test.py", "r") as source:
    tree = ast.parse(source.read())

for node in ast.iter_child_nodes(tree):
    if _isClassDef(node):
        findUnitTestClass(node)
