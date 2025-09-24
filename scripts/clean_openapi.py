import re

file_path = "/home/heitor/Repositories/mintlify/fuel50-docs/openapi.test"
output_lines = []
in_method_content = False
method_indentation = 0

with open(file_path, "r") as f:
    lines = f.readlines()

for line in lines:
    stripped_line = line.lstrip()
    current_indentation = len(line) - len(stripped_line)

    # Check for endpoint (starts with / and has a colon at the end, after stripping)
    if stripped_line.startswith('/') and stripped_line.endswith(':\n'):
        output_lines.append(line)
        in_method_content = False  # Reset flag for new endpoint
    # Check for HTTP method (get, post, put, delete, patch followed by :)
    elif re.match(r'^(get|post|put|delete|patch):\s*\n$', stripped_line):
        output_lines.append(line)
        in_method_content = True
        method_indentation = current_indentation
    elif in_method_content and current_indentation > method_indentation:
        # Skip lines that are part of the method's content
        continue
    else:
        # Not an endpoint, not a method, and not a line to skip (or end of method content)
        output_lines.append(line)
        in_method_content = False  # Reset flag if indentation is less or equal

with open(file_path, "w") as f:
    f.writelines(output_lines)