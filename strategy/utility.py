import ast


class TopLevelVariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.current_scope = None

    def visit_Assign(self, node):
        # Only collect assignments if they are in the top-level scope
        if self.current_scope is None:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variables.add(target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Entering a function scope, stop collecting variables
        self.current_scope = 'function'
        self.generic_visit(node)
        self.current_scope = None  # Exit function scope

    def visit_ClassDef(self, node):
        # Entering a class scope, stop collecting variables
        self.current_scope = 'class'
        self.generic_visit(node)
        self.current_scope = None  # Exit class scope


def find_declared_variables(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)

    visitor = TopLevelVariableVisitor()
    visitor.visit(tree)
    return visitor.variables
s