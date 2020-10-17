import ast
from contextlib import contextmanager
from types import ModuleType
from typing import List
import test
import inspect


class Reader:

    @staticmethod
    @contextmanager
    def read(testModuleName: str):
        pass

    def _findPathModule(self, path: str):
        pass


with open("test.py", "r") as source:
    tree = ast.parse(source.read())

source = inspect.getsource(test)


def findUnitTestClass(classNode: ast.ClassDef):
    def _isUnitTest(base: List[expr]) -> bool:
        return base.value.id == 'unittest' and base.attr == 'TestCase'

    if not any(_isUnitTest, classNode.bases):
        return False

    for node in ast.iter_child_nodes(classNode):
        if isinstance(node, ast.FunctionDef):


for node in ast.iter_child_nodes(tree):
    if isinstance(node, ast.ClassDef):
        findUnitTestClass(node)
