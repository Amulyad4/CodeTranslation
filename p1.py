import re

def java_to_python(java_code):
    lines = java_code.strip().split('\n')
    python_lines = []

    indent_level = 0
    indent = lambda: '    ' * indent_level
    class_name = ''
    inside_class = False
    inside_method = False

    for line in lines:
        line = line.strip()

        if not line:
            python_lines.append('')
            continue

        # Handle class definition
        match = re.match(r'public\s+class\s+(\w+)', line)
        if match:
            class_name = match.group(1)
            python_lines.append(f'class {class_name}:')
            indent_level += 1
            inside_class = True
            continue

        # Handle constructor
        match = re.match(r'public\s+' + class_name + r'\((.*?)\)', line)
        if match:
            args = match.group(1)
            args = re.sub(r'\b(String|int|double|boolean)\s+', '', args)
            args = args.strip()
            args_list = ['self'] + [a.strip() for a in args.split(',')] if args else ['self']
            python_lines.append(indent() + f'def __init__({", ".join(args_list)}):')
            indent_level += 1
            inside_method = True
            continue

        # Handle method definition
        match = re.match(r'public\s+void\s+(\w+)\((.*?)\)', line)
        if match:
            method_name, args = match.groups()
            args = re.sub(r'\b(String|int|double|boolean)\s+', '', args)
            args = args.strip()
            args_list = ['self'] + [a.strip() for a in args.split(',')] if args else ['self']
            python_lines.append(indent() + f'def {method_name}({", ".join(args_list)}):')
            indent_level += 1
            inside_method = True
            continue

        # Handle print statements
        if 'System.out.println' in line:
            content = re.findall(r'System\.out\.println\((.*)\);', line)
            if content:
                python_lines.append(indent() + f'print({content[0]})')
            continue
        elif 'System.out.print' in line:
            content = re.findall(r'System\.out\.print\((.*)\);', line)
            if content:
                python_lines.append(indent() + f'print({content[0]}, end="")')
            continue

        # Variable declarations
        line = re.sub(r'\b(int|double|float|String|boolean)\b\s+', '', line)
        line = line.replace("true", "True").replace("false", "False")
        line = line.replace(';', '')

        # Convert this. to self.
        line = line.replace('this.', 'self.')

        # Closing brace
        if line == '}':
            indent_level = max(0, indent_level - 1)
            if indent_level == 1:
                inside_method = False
            continue

        python_lines.append(indent() + line)

    return '\n'.join(python_lines)
