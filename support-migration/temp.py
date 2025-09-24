import json

def process_items(items, file_handle, indent_level=0):
    """
    Recursively processes items (folders or requests) from a Postman collection
    and writes them to the output file.
    """
    # Create an indentation string based on the current depth
    indent = "  " * indent_level

    for item in items:
        # Check if the item is a folder (it will have an 'item' key)
        if "item" in item:
            # It's a folder, so write its name
            file_handle.write(f"{indent}📁 {item.get('name', 'Untitled Folder')}\n")
            # Recursively process the items inside this folder
            process_items(item["item"], file_handle, indent_level + 1)
        
        # Otherwise, it's a request (it will have a 'request' key)
        elif "request" in item:
            request = item["request"]
            method = request.get("method", "METHOD_NOT_FOUND")
            
            # The URL can be a string or a dictionary. We get the 'raw' version.
            url_data = request.get("url", {})
            url = url_data.get("raw", "URL_NOT_FOUND") if isinstance(url_data, dict) else url_data

            # Write the formatted request details
            # file_handle.write(f"{indent}  - [{method}] {item.get('name', 'Untitled Request')}\n")
            # file_handle.write(f"{indent}    URL: {url}\n")
            file_handle.write(f"{indent}  - {method} {url}\n")


def generate_list_from_postman(input_json_file='collection.json', output_txt_file='postman_endpoints.txt'):
    """
    Parses a Postman collection JSON file and generates a structured text file
    listing all folders and endpoints.
    """
    try:
        # Open and load the JSON file
        with open(input_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Open the output file for writing
        with open(output_txt_file, 'w', encoding='utf-8') as f_out:
            collection_name = data.get("info", {}).get("name", "Postman Collection")
            f_out.write(f"Endpoints for: {collection_name}\n")
            f_out.write("=" * (18 + len(collection_name)) + "\n\n")

            # Start the recursive processing from the top-level items
            if "item" in data:
                process_items(data["item"], f_out)
            else:
                f_out.write("No items found in the collection.")

        print(f"✅ Success! Endpoint list has been exported to {output_txt_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_json_file}' was not found. Please export it from Postman.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON. Is '{input_json_file}' a valid JSON file?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    generate_list_from_postman()