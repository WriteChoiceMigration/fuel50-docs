
import re

def extract_endpoints_and_methods(yaml_content):
    endpoints_data = {}
    current_endpoint = None
    in_paths_section = False
    paths_indentation = -1
    endpoint_indentation = -1

    lines = yaml_content.splitlines()
    for line in lines:
        stripped_line = line.lstrip()
        current_indentation = len(line) - len(stripped_line)

        if stripped_line == "paths:":
            in_paths_section = True
            paths_indentation = current_indentation
            continue

        if in_paths_section:
            if current_indentation <= paths_indentation and stripped_line != "paths:":
                in_paths_section = False
                current_endpoint = None
                endpoint_indentation = -1
                continue

            # Check for endpoint path (e.g., /path/to/resource:)
            # It should start with / and be indented 2 spaces more than 'paths:'
            if re.match(r'^/[a-zA-Z0-9/{}-]+:\s*$', stripped_line) and current_indentation == paths_indentation + 2:
                current_endpoint = stripped_line.rstrip(':').strip()
                endpoints_data[current_endpoint] = []
                endpoint_indentation = current_indentation
                continue

            # Check for HTTP method (get, post, put, delete, patch followed by :)
            # It should be indented 2 spaces more than the current endpoint
            if current_endpoint and re.match(r'^(get|post|put|delete|patch):\s*$', stripped_line) and current_indentation == endpoint_indentation + 2:
                method = stripped_line.rstrip(':').strip()
                endpoints_data[current_endpoint].append(method)
                continue

    return endpoints_data


file_path = "/home/heitor/Repositories/mintlify/fuel50-docs/openapi.yaml"
output_file_path = "/home/heitor/Repositories/mintlify/fuel50-docs/endpoints.txt"

with open(file_path, "r") as f:
    yaml_content = f.read()

endpoints_and_methods = extract_endpoints_and_methods(yaml_content)

output_lines = []
for endpoint, methods in endpoints_and_methods.items():
    output_lines.append(f"Endpoint: {endpoint}")
    if methods:
        for method in methods:
            output_lines.append(f"  - {method.upper()}")
    else:
        output_lines.append("  No HTTP methods found.")
    output_lines.append("\n")

with open(output_file_path, "w") as f:
    f.writelines(output_lines)
