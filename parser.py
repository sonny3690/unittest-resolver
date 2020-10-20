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


class Context(defaultdict):
    def __init__(self, *, obj=None, name='global'):
        super().__init__(list)

        self.__parent = None
        self.__children = []

        # name should be immutable
        self._obj: ast = obj
        self._name: str = name

        # defined in the constructor since it's an immutable property
        self.isTestingContext = isinstance(
            obj, ast.ClassDef) and Context.__checkClassBase(obj)

    @staticmethod
    def __checkClassBase(node: ast.ClassDef) -> bool:
        return any(map(lambda base: base.value.id == 'unittest' and base.attr == 'TestCase', node.bases))

    @property
    def _parent(self):
        return self.__parent

    @property
    def _children(self):
        return self.__children

    @property
    def obj(self):
        return self._obj

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
        return prefix + '#' + self._name


class Declaration:
    def __init__(self, source: ast, name: str):
        self.source = source
        self.name = name
        self.references = []

    def __repr__(self):
        return "{} w/ references {}".format(self.name, self.references)


_global_context = Context()


@lru_cache(maxsize=100)
def encodeID(name: str, context: Context):
    return base64.b64encode(context.path + '#' + name)


@lru_cache(maxsize=100)
def decodeID(id: str):
    return base64.b64decode(id).split('#')[-1]


def _extractFunctionCall(node: ast.Call, context: Context):
    referenceFunctionName = node.func.id

    # essentially, we climb our context to find the most appropriate one
    while context != None:

        if referenceFunctionName in context:
            context[referenceFunctionName].references.append(node)
            return

        context = context._parent

    print("Could not find function for {}".format(node.func.id))


def swapContext(parentContext: Context, node: ast) -> Tuple[Context, Context]:
    context = Context(obj=node, name=node.name)
    parentContext.addChild(context)

    context.isTestingContext = parentContext.isTestingContext or context.isTestingContext
    parentContext[node.name] = Declaration(node, node.name)

    return parentContext, context


def findTestCaseCalls(node: ast, context: Context = _global_context):

    if _isScopeCreator(node):
        print('creating scope for ', node.name)
        # we ought to keep looking through oulr queue, especially through our new citizens
        _, context = swapContext(context, node)

    elif _isCall(node) and context.isTestingContext:
        _extractFunctionCall(node, context)

    for nextNode in ast.iter_child_nodes(node):
        findTestCaseCalls(nextNode, context)


def findUnitTestClass(node: ast.ClassDef):
    findTestCaseCalls(node)


# main thread starter that starts everything
def doWork():
    with open("test.py", "r") as source:
        tree = ast.parse(source.read())

    # just look one level down for the test
    for node in ast.iter_child_nodes(tree):
        findUnitTestClass(node)

    stack = [_global_context]

    while stack:
        context = stack.pop()

        stack.extend(context._children)


doWork()
