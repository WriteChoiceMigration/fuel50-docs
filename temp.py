import yaml

def generate_endpoints_list(input_yaml_file='openapi.yaml', output_txt_file='endpoints.txt'):
    """
    Parses an OpenAPI YAML file to extract endpoints and their HTTP methods,
    and writes them to a text file.

    Args:
        input_yaml_file (str): The name of the input OpenAPI file.
        output_txt_file (str): The name of the output text file.
    """
    try:
        # Open and safely load the YAML file into a Python dictionary
        with open(input_yaml_file, 'r', encoding='utf-8') as f:
            openapi_data = yaml.safe_load(f)

        # Ensure the 'paths' key exists in the YAML file
        if 'paths' not in openapi_data:
            print(f"Error: The key 'paths' was not found in {input_yaml_file}.")
            return

        paths = openapi_data['paths']

        # Open the output file in write mode
        with open(output_txt_file, 'w', encoding='utf-8') as f_out:
            f_out.write("API Endpoints and Available Methods\n")
            f_out.write("=" * 35 + "\n\n")

            # Iterate through each path (endpoint) and its defined methods
            for path, methods in paths.items():
                # The 'path' variable holds the endpoint string (e.g., '/users/{id}')
                f_out.write(f"Endpoint: {path}\n")
                
                # The 'methods' variable is a dictionary of HTTP methods (get, post, etc.)
                http_methods = [method.upper() for method in methods.keys()]
                
                for method in http_methods:
                    f_out.write(f"  - {method}\n")
                
                f_out.write("\n") # Add a blank line for better readability

        print(f"✅ Success! Endpoint list has been exported to {output_txt_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_yaml_file}' was not found. Please ensure it's in the same directory.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    generate_endpoints_list()