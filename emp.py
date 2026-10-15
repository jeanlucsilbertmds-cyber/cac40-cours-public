import ast, hashlib, sys
def empreinte(src):
    a = ast.parse(src)
    for n in ast.walk(a):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if (n.body and isinstance(n.body[0], ast.Expr)
                    and isinstance(n.body[0].value, ast.Constant)
                    and isinstance(n.body[0].value.value, str)):
                n.body = n.body[1:]
    return hashlib.sha256(ast.dump(a).encode()).hexdigest()[:16]
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"{empreinte(open(p,encoding='utf-8').read())}  {p}")
