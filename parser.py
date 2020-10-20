import ast
from contextlib import contextmanager
from types import ModuleType
from typing import List, Generator, Tuple
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

        # name should be immutable
        self.__name = name

    @property
    def _parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

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

    @property
    def path(self):
        prefix = (self.__parent.path if self.__parent else '')
        return prefix + '#' + self.__name


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
    ...


_global_context = Context()
_references = defaultdict(list)


@lru_cache(maxsize=100)
def encodeID(name: str, context: Context):
    return base64.b64encode(context.path + name)


@lru_cache(maxsize=100)
def decodeID(id: str):
    return base64.b64decode(id).split('#')[-1]


def _extractFunctionCall(node: ast.Call, context: Context):
    referenceFunctionName = node.func.id

    # essentially, we climb our context to find the most appropriate one
    while context != None:
        if hasattr(context, referenceFunctionName):
            context[referenceFunctionName].append(node)
            return

        context = context._parent

    print("Could not find function for {}".format(node.func.id))


def swapContext(parentContext: Context) -> Tuple[Context, Context]:
    context = Context()
    parentContext.addChild(context)
    return parentContext, context


def findTestCaseCalls(node: ast, context: Context = _global_context):
    if _isScopeCreator(node):
        # we ought to keep looking through oulr queue, especially through our new citizens
        print(node.name)
        _, context = swapContext(context)

    elif _isCall(node):
        _extractFunctionCall(node, context)

    for nextNode in ast.iter_child_nodes(node):
        findTestCaseCalls(nextNode, context)


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
