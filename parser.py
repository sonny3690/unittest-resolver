import ast
from contextlib import contextmanager
from types import ModuleType
from typing import List, Generator
import test
import inspect
from collections import defaultdict, deque
from typeguards import _isClassDef, _isScopeCreator, _isFunctionDef, _isCall
import itertools
from collections import defaultdict
import base64
from functools import lru_cache


class Context(dict):
    def __init__(self, *, parent=None, name='global'):
        self.__parent = parent
        self.__children = []
        self.__name = name

    @property
    def _parent(self):
        return self.__parent

    @_parent.setter
    def _parent(self, parent):
        assert(parent is not None)
        self.__parent = parent

    def addChild(self, child: dict):
        child._parent = self
        self.__children.append(child)

    def addNode(self, node: ast):
        if _isClassDef(node):
            self['class'] = node
        elif _isFunctionDef(node):
            self['function'] = node


class DeclarationMap(defaultdict):
    '''
    Mapping of declarationID to references in the form of ast nodes.

    It's not collision proof unfortunately, but we'll have to do without it for now.
    '''
    ...


class idMap(dict):
    '''
    Maps declarationID to node
    '''


@lru_cache(maxsize=100)
def encodeID(name: str):
    return base64.b64encode(name)


@lru_cache(maxsize=100)
def decodeID(id: str):
    return base64.b64decode(id)


_global_context = Context()
_references = defaultdict(list)


def _extractFunctionCalls(node: ast):
    pass


def findTestCaseCalls(node: ast, context: Context = _global_context):
    queue: Generator = iter([node])
    prevContext, currContext = context, context

    while True:
        try:
            curr = next(queue)
            if _isScopeCreator(curr):
                # we ought to keep looking
                queue = itertools.chain(ast.iter_child_nodes(curr))
            elif _isCall(curr):
                # storeCall()
                pass

        except StopIteration:
            break


def findUnitTestClass(node: ast.ClassDef):

    # unit test identifier
    def _isUnitTest(base: List[ast.expr]) -> bool:
        return base.value.id == 'unittest' and base.attr == 'TestCase'

    if _isClassDef(node):
        if not any(map(_isUnitTest, node.bases)):
            return False
        findTestCaseCalls(node)


# main thread starter that starts everything
def doWork():
    with open("test.py", "r") as source:
        tree = ast.parse(source.read())

    # just look one level down for the test
    for node in ast.iter_child_nodes(tree):
        findUnitTestClass(node)


doWork()
