from p1 import java_to_python
from p2 import python_to_java
from p3 import c_to_python
from p4 import python_to_c
from p5 import java_to_c
from p6 import c_to_java

# Mapping functions to string keys
translator_map = {
    ('java', 'python'): java_to_python,
    ('python', 'java'): python_to_java,
    ('c', 'python'): c_to_python,
    ('python', 'c'): python_to_c,
    ('java', 'c'): java_to_c,
    ('c', 'java'): c_to_java,
}

# === Ask user input ===
from_lang = input("Enter source language (java/c/python): ").strip().lower()
to_lang = input("Enter target language (java/c/python): ").strip().lower()

if (from_lang, to_lang) not in translator_map:
    print("❌ Translation between these languages is not supported yet.")
else:
    print("Enter your code (type 'END' to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    code_input = "\n".join(lines)

    # Call appropriate translator function
    translate_function = translator_map[(from_lang, to_lang)]
    output = translate_function(code_input)

    print("\n=== Translated Code ===")
    print(output)
