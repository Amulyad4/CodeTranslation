from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import re
import ast
import javalang
import esprima

app = Flask(__name__)
CORS(app)

class AdvancedTranslator:
    def __init__(self):
        pass

    def translate(self, source_code, source_lang, target_lang):
        if source_lang == target_lang:
            return source_code

        translation_map = {
            # Python translations
            ('python', 'java'): self._python_to_java,
            ('python', 'cpp'): self._python_to_cpp,
            ('python', 'c'): self._python_to_c,
            ('python', 'javascript'): self._python_to_js,
            
            # Java translations
            ('java', 'python'): self._java_to_python,
            ('java', 'c'): self._java_to_c,
            ('java', 'cpp'): self._java_to_cpp,
            ('java', 'javascript'): self._java_to_js,
            
            # C translations
            ('c', 'python'): self._c_to_python,
            ('c', 'java'): self._c_to_java,
            ('c', 'cpp'): self._c_to_cpp,
            ('c', 'javascript'): self._c_to_js,
            
            # C++ translations
            ('cpp', 'python'): self._cpp_to_python,
            ('cpp', 'java'): self._cpp_to_java,
            ('cpp', 'c'): self._cpp_to_c,
            ('cpp', 'javascript'): self._cpp_to_js,
            
            # JavaScript translations
            ('javascript', 'python'): self._js_to_python,
            ('javascript', 'java'): self._js_to_java,
            ('javascript', 'c'): self._js_to_c,
            ('javascript', 'cpp'): self._js_to_cpp,
        }
        
        try:
            if (source_lang, target_lang) in translation_map:
                return translation_map[(source_lang, target_lang)](source_code)
            return f"// Translation from {source_lang} to {target_lang} not implemented\n{source_code}"
        except Exception as e:
            comment_char = '#' if target_lang in ['python'] else '//'
            return f"{comment_char} Error: {str(e)}\n{source_code}"

    # ================== Python Conversions ==================
    def _python_to_java(self, code):
        try:
            py_ast = ast.parse(code)
            java_code = ["public class Main {", "    public static void main(String[] args) {"]
            
            for node in py_ast.body:
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
                        args = ', ". "'.join(self._py_expr_to_java(arg) for arg in node.value.args)
                        java_code.append(f'        System.out.println({args});')
                
                elif isinstance(node, ast.FunctionDef):
                    return_type = "Object"
                    params = ', '.join(f'Object {arg.arg}' for arg in node.args.args)
                    java_code.append(f'    public static {return_type} {node.name}({params}) {{')
                    java_code.append('        // Function body not translated')
                    java_code.append('        return null;')
                    java_code.append('    }')
            
            java_code.append("    }")
            java_code.append("}")
            return '\n'.join(java_code)
        except Exception as e:
            raise Exception(f"Python to Java: {str(e)}")

    def _python_to_cpp(self, code):
        try:
            cpp_code = ["#include <iostream>", "using namespace std;", ""]
            py_ast = ast.parse(code)
            
            for node in py_ast.body:
                if isinstance(node, ast.FunctionDef):
                    params = ', '.join(f'auto {arg.arg}' for arg in node.args.args)
                    cpp_code.append(f'auto {node.name}({params}) {{')
                    cpp_code.append('    // Function body not translated')
                    cpp_code.append('}')
                
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
                        args = ' << " " << '.join(self._py_expr_to_cpp(arg) for arg in node.value.args)
                        cpp_code.append(f'    cout << {args} << endl;')
            
            return '\n'.join(cpp_code)
        except Exception as e:
            raise Exception(f"Python to C++: {str(e)}")

    def _python_to_c(self, code):
        try:
            c_code = ["#include <stdio.h>", ""]
            py_ast = ast.parse(code)
            
            for node in py_ast.body:
                if isinstance(node, ast.FunctionDef):
                    c_code.append(f'void {node.name}() {{')
                    c_code.append('    // Function body not translated')
                    c_code.append('}')
                
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
                        args = ', '.join(self._py_expr_to_c(arg) for arg in node.value.args)
                        c_code.append(f'    printf({args});')
            
            return '\n'.join(c_code)
        except Exception as e:
            raise Exception(f"Python to C: {str(e)}")

    def _python_to_js(self, code):
        try:
            js_code = []
            py_ast = ast.parse(code)
            
            for node in py_ast.body:
                if isinstance(node, ast.FunctionDef):
                    params = ', '.join(arg.arg for arg in node.args.args)
                    js_code.append(f'function {node.name}({params}) {{')
                    js_code.append('    // Function body not translated')
                    js_code.append('}')
                
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
                        args = ', '.join(self._py_expr_to_js(arg) for arg in node.value.args)
                        js_code.append(f'console.log({args});')
            
            return '\n'.join(js_code)
        except Exception as e:
            raise Exception(f"Python to JS: {str(e)}")

    # ================== Java Conversions ==================
    def _java_to_python(self, code):
        try:
            tree = javalang.parse.parse(code)
            py_code = []
            
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    if node.name == 'main':
                        py_code.append('if __name__ == "__main__":')
                        for stmt in node.body:
                            if (isinstance(stmt, javalang.tree.MethodInvocation) and
                                stmt.qualifier == 'System.out' and
                                stmt.member == 'println'):
                                args = ', '.join(self._java_expr_to_py(arg) for arg in stmt.arguments)
                                py_code.append(f'    print({args})')
            
            return '\n'.join(py_code)
        except Exception as e:
            raise Exception(f"Java to Python: {str(e)}")

    def _java_to_c(self, code):
        try:
            c_code = ["#include <stdio.h>", ""]
            tree = javalang.parse.parse(code)
            
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    if node.name == 'main':
                        c_code.append('int main() {')
                        for stmt in node.body:
                            if (isinstance(stmt, javalang.tree.MethodInvocation) and
                                stmt.qualifier == 'System.out' and
                                stmt.member == 'println'):
                                args = ', '.join(self._java_expr_to_c(arg) for arg in stmt.arguments)
                                c_code.append(f'    printf({args});')
                        c_code.append('}')
            
            return '\n'.join(c_code)
        except Exception as e:
            raise Exception(f"Java to C: {str(e)}")

    def _java_to_cpp(self, code):
        try:
            cpp_code = ["#include <iostream>", "using namespace std;", ""]
            tree = javalang.parse.parse(code)
            
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    if node.name == 'main':
                        cpp_code.append('int main() {')
                        for stmt in node.body:
                            if (isinstance(stmt, javalang.tree.MethodInvocation) and
                                stmt.qualifier == 'System.out' and
                                stmt.member == 'println'):
                                args = ' << " " << '.join(self._java_expr_to_cpp(arg) for arg in stmt.arguments)
                                cpp_code.append(f'    cout << {args} << endl;')
                        cpp_code.append('}')
            
            return '\n'.join(cpp_code)
        except Exception as e:
            raise Exception(f"Java to C++: {str(e)}")

    def _java_to_js(self, code):
        try:
            js_code = []
            tree = javalang.parse.parse(code)
            
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    if node.name == 'main':
                        js_code.append('// Main function')
                        for stmt in node.body:
                            if (isinstance(stmt, javalang.tree.MethodInvocation) and
                                stmt.qualifier == 'System.out' and
                                stmt.member == 'println'):
                                args = ', '.join(self._java_expr_to_js(arg) for arg in stmt.arguments)
                                js_code.append(f'console.log({args});')
            
            return '\n'.join(js_code)
        except Exception as e:
            raise Exception(f"Java to JS: {str(e)}")

    # ================== C Conversions ==================
    def _c_to_python(self, code):
        try:
            py_code = []
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    py_code.append('if __name__ == "__main__":')
                    in_main = True
                elif in_main and 'printf(' in line:
                    args = re.search(r'printf\((.*?)\);', line)
                    if args:
                        py_code.append(f'    print({args.group(1)})')
            
            return '\n'.join(py_code)
        except Exception as e:
            raise Exception(f"C to Python: {str(e)}")

    def _c_to_java(self, code):
        try:
            java_code = ["public class Main {", "    public static void main(String[] args) {"]
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    in_main = True
                elif in_main and 'printf(' in line:
                    args = re.search(r'printf\((.*?)\);', line)
                    if args:
                        java_code.append(f'        System.out.println({args.group(1)});')
            
            java_code.append("    }")
            java_code.append("}")
            return '\n'.join(java_code)
        except Exception as e:
            raise Exception(f"C to Java: {str(e)}")

    def _c_to_cpp(self, code):
        try:
            cpp_code = ["#include <iostream>", "using namespace std;", ""]
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    cpp_code.append('int main() {')
                    in_main = True
                elif in_main and 'printf(' in line:
                    args = re.search(r'printf\((.*?)\);', line)
                    if args:
                        cpp_code.append(f'    cout << {args.group(1)} << endl;')
                elif '#include' in line and 'stdio' in line:
                    continue
                else:
                    cpp_code.append(line)
            
            return '\n'.join(cpp_code)
        except Exception as e:
            raise Exception(f"C to C++: {str(e)}")

    def _c_to_js(self, code):
        try:
            js_code = []
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    js_code.append('// Main function')
                    in_main = True
                elif in_main and 'printf(' in line:
                    args = re.search(r'printf\((.*?)\);', line)
                    if args:
                        js_code.append(f'console.log({args.group(1)});')
            
            return '\n'.join(js_code)
        except Exception as e:
            raise Exception(f"C to JS: {str(e)}")

    # ================== C++ Conversions ==================
    def _cpp_to_python(self, code):
        try:
            py_code = []
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    py_code.append('if __name__ == "__main__":')
                    in_main = True
                elif in_main and 'cout <<' in line:
                    parts = line.split('<<')
                    args = []
                    for part in parts[1:-1]:
                        args.append(part.strip())
                    py_code.append(f'    print({" ".join(args)})')
            
            return '\n'.join(py_code)
        except Exception as e:
            raise Exception(f"C++ to Python: {str(e)}")

    def _cpp_to_java(self, code):
        try:
            java_code = ["public class Main {", "    public static void main(String[] args) {"]
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    in_main = True
                elif in_main and 'cout <<' in line:
                    parts = line.split('<<')
                    args = []
                    for part in parts[1:-1]:
                        args.append(part.strip())
                    java_code.append(f'        System.out.println({" ".join(args)});')
            
            java_code.append("    }")
            java_code.append("}")
            return '\n'.join(java_code)
        except Exception as e:
            raise Exception(f"C++ to Java: {str(e)}")

    def _cpp_to_c(self, code):
        try:
            c_code = ["#include <stdio.h>", ""]
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    c_code.append('int main() {')
                    in_main = True
                elif in_main and 'cout <<' in line:
                    parts = line.split('<<')
                    args = []
                    for part in parts[1:-1]:
                        args.append(part.strip())
                    c_code.append(f'    printf({" ".join(args)});')
                elif '#include <iostream>' in line:
                    continue
                elif 'using namespace std;' in line:
                    continue
                else:
                    c_code.append(line)
            
            return '\n'.join(c_code)
        except Exception as e:
            raise Exception(f"C++ to C: {str(e)}")

    def _cpp_to_js(self, code):
        try:
            js_code = []
            in_main = False
            
            for line in code.split('\n'):
                if 'int main(' in line:
                    js_code.append('// Main function')
                    in_main = True
                elif in_main and 'cout <<' in line:
                    parts = line.split('<<')
                    args = []
                    for part in parts[1:-1]:
                        args.append(part.strip())
                    js_code.append(f'console.log({" ".join(args)});')
            
            return '\n'.join(js_code)
        except Exception as e:
            raise Exception(f"C++ to JS: {str(e)}")

    # ================== JavaScript Conversions ==================
    def _js_to_python(self, code):
        try:
            py_code = []
            js_ast = esprima.parseScript(code)
            
            for node in js_ast.body:
                if node.type == 'ExpressionStatement' and \
                   node.expression.type == 'CallExpression' and \
                   node.expression.callee.object and \
                   node.expression.callee.object.name == 'console' and \
                   node.expression.callee.property.name == 'log':
                    args = ', '.join(self._js_expr_to_py(arg) for arg in node.expression.arguments)
                    py_code.append(f'print({args})')
                
                elif node.type == 'FunctionDeclaration':
                    params = ', '.join(param.name for param in node.params)
                    py_code.append(f'def {node.id.name}({params}):')
                    py_code.append('    pass')
            
            return '\n'.join(py_code)
        except Exception as e:
            raise Exception(f"JS to Python: {str(e)}")

    def _js_to_java(self, code):
        try:
            java_code = ["public class Main {", "    public static void main(String[] args) {"]
            js_ast = esprima.parseScript(code)
            
            for node in js_ast.body:
                if node.type == 'ExpressionStatement' and \
                   node.expression.type == 'CallExpression' and \
                   node.expression.callee.object and \
                   node.expression.callee.object.name == 'console' and \
                   node.expression.callee.property.name == 'log':
                    args = ', ". "'.join(self._js_expr_to_java(arg) for arg in node.expression.arguments)
                    java_code.append(f'        System.out.println({args});')
            
            java_code.append("    }")
            java_code.append("}")
            return '\n'.join(java_code)
        except Exception as e:
            raise Exception(f"JS to Java: {str(e)}")

    def _js_to_c(self, code):
        try:
            c_code = ["#include <stdio.h>", ""]
            js_ast = esprima.parseScript(code)
            
            for node in js_ast.body:
                if node.type == 'ExpressionStatement' and \
                   node.expression.type == 'CallExpression' and \
                   node.expression.callee.object and \
                   node.expression.callee.object.name == 'console' and \
                   node.expression.callee.property.name == 'log':
                    args = ', '.join(self._js_expr_to_c(arg) for arg in node.expression.arguments)
                    c_code.append(f'    printf({args});')
            
            return '\n'.join(c_code)
        except Exception as e:
            raise Exception(f"JS to C: {str(e)}")

    def _js_to_cpp(self, code):
        try:
            cpp_code = ["#include <iostream>", "using namespace std;", ""]
            js_ast = esprima.parseScript(code)
            
            for node in js_ast.body:
                if node.type == 'ExpressionStatement' and \
                   node.expression.type == 'CallExpression' and \
                   node.expression.callee.object and \
                   node.expression.callee.object.name == 'console' and \
                   node.expression.callee.property.name == 'log':
                    args = ' << " " << '.join(self._js_expr_to_cpp(arg) for arg in node.expression.arguments)
                    cpp_code.append(f'    cout << {args} << endl;')
            
            return '\n'.join(cpp_code)
        except Exception as e:
            raise Exception(f"JS to C++: {str(e)}")

    # ================== Expression Converters ==================
    def _py_expr_to_java(self, expr):
        if isinstance(expr, ast.Str):
            return f'"{expr.s}"'
        elif isinstance(expr, ast.Num):
            return str(expr.n)
        elif isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.JoinedStr):
            parts = []
            for value in expr.values:
                if isinstance(value, ast.Str):
                    parts.append(value.s)
                elif isinstance(value, ast.FormattedValue):
                    parts.append('%s')
                    parts.append(self._py_expr_to_java(value.value))
            return '"' + ''.join(parts) + '"'
        return "/* Unsupported expression */"

    def _py_expr_to_cpp(self, expr):
        if isinstance(expr, ast.Str):
            return f'"{expr.s}"'
        elif isinstance(expr, ast.Num):
            return str(expr.n)
        elif isinstance(expr, ast.Name):
            return expr.id
        return "/* Unsupported expression */"

    def _py_expr_to_c(self, expr):
        if isinstance(expr, ast.Str):
            return f'"{expr.s}"'
        elif isinstance(expr, ast.Num):
            return str(expr.n)
        elif isinstance(expr, ast.Name):
            return expr.id
        return "/* Unsupported expression */"

    def _py_expr_to_js(self, expr):
        if isinstance(expr, ast.Str):
            return f'"{expr.s}"'
        elif isinstance(expr, ast.Num):
            return str(expr.n)
        elif isinstance(expr, ast.Name):
            return expr.id
        return "/* Unsupported expression */"

    def _java_expr_to_py(self, expr):
        if isinstance(expr, javalang.tree.Literal):
            if expr.value == 'null':
                return 'None'
            elif expr.value in ('true', 'false'):
                return expr.value.capitalize()
            return expr.value
        elif isinstance(expr, javalang.tree.MemberReference):
            if expr.qualifier:
                return f"{expr.qualifier}.{expr.member}"
            return expr.member
        return "# Unsupported expression"

    def _java_expr_to_c(self, expr):
        if isinstance(expr, javalang.tree.Literal):
            return expr.value
        elif isinstance(expr, javalang.tree.MemberReference):
            if expr.qualifier:
                return f"{expr.qualifier}.{expr.member}"
            return expr.member
        return "/* Unsupported expression */"

    def _java_expr_to_cpp(self, expr):
        if isinstance(expr, javalang.tree.Literal):
            return expr.value
        elif isinstance(expr, javalang.tree.MemberReference):
            if expr.qualifier:
                return f"{expr.qualifier}.{expr.member}"
            return expr.member
        return "/* Unsupported expression */"

    def _java_expr_to_js(self, expr):
        if isinstance(expr, javalang.tree.Literal):
            if expr.value == 'null':
                return 'null'
            elif expr.value in ('true', 'false'):
                return expr.value
            return expr.value
        elif isinstance(expr, javalang.tree.MemberReference):
            if expr.qualifier:
                return f"{expr.qualifier}.{expr.member}"
            return expr.member
        return "/* Unsupported expression */"

    def _js_expr_to_py(self, expr):
        if expr.type == 'Literal':
            if expr.value == 'null':
                return 'None'
            elif expr.value in ('true', 'false'):
                return expr.value.capitalize()
            return expr.value
        elif expr.type == 'Identifier':
            return expr.name
        return "# Unsupported expression"

    def _js_expr_to_java(self, expr):
        if expr.type == 'Literal':
            if expr.value == 'null':
                return 'null'
            elif expr.value in ('true', 'false'):
                return expr.value
            return expr.value
        elif expr.type == 'Identifier':
            return expr.name
        return "/* Unsupported expression */"

    def _js_expr_to_c(self, expr):
        if expr.type == 'Literal':
            return expr.value
        elif expr.type == 'Identifier':
            return expr.name
        return "/* Unsupported expression */"

    def _js_expr_to_cpp(self, expr):
        if expr.type == 'Literal':
            return expr.value
        elif expr.type == 'Identifier':
            return expr.name
        return "/* Unsupported expression */"

# Initialize translator
translator = AdvancedTranslator()

@app.route('/translate', methods=['POST'])
def handle_translation():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
        
    data = request.get_json()
    
    required_fields = ['code', 'source_lang', 'target_lang']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    try:
        translated_code = translator.translate(
            data['code'],
            data['source_lang'],
            data['target_lang']
        )
        
        return jsonify({
            'translated_code': translated_code,
            'source_lang': data['source_lang'],
            'target_lang': data['target_lang']
        })
    except Exception as e:
        app.logger.error(f"Translation error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)