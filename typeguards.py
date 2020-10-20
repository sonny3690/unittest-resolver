import ast


# applies for lambda functions
def _isFunctionDef(node: any) -> bool: return isinstance(node, ast.FunctionDef)


def _isClassDef(node: any) -> bool: return isinstance(node, ast.ClassDef)


def _isCall(node: any) -> bool: return isinstance(node, ast.Call)


def _isScopeCreator(node: any) -> bool:
    return _isFunctionDef(node) or _isClassDef(node)
