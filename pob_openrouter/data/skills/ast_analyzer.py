import ast
import sys

def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, ast.FunctionDef):
        print(f"{indent}├── 🛠️ Function: {node.name} (Args: {len(node.args.args)})")
    elif isinstance(node, ast.ClassDef):
        print(f"{indent}├── 🏛️ Class: {node.name}")
    elif isinstance(node, ast.AsyncFunctionDef):
        print(f"{indent}├── ⚡ AsyncFunction: {node.name} (Args: {len(node.args.args)})")
        
    # 递归遍历子节点中的方法/类
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            print_tree(child, level + 1)

def analyze(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        print(f"=== AST Topology of {filepath} ===")
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                print_tree(node)
    except Exception as e:
        print(f"❌ Error parsing AST: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        analyze(sys.argv[1])
