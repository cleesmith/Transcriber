import sys
import base64
import gzip
import json
from typing import Any, Dict


def decode_compressed_prompt(compressed_string):
    """
    Decodes a base64-encoded, gzip-compressed string.
    Args:
        compressed_string (str): The base64-encoded, gzip-compressed string
    Returns:
        str: The decoded and decompressed string
    Raises:
        ValueError: If the input string is not valid base64 or gzip-compressed data
    """
    try:
        # Step 1: Decode the base64 string to bytes
        base64_decoded = base64.b64decode(compressed_string)
        
        # Step 2: Decompress the gzip data
        decompressed_data = gzip.decompress(base64_decoded)
        
        # Step 3: Decode the bytes to string using UTF-8
        decoded_string = decompressed_data.decode('utf-8')
        
        return decoded_string
        
    except base64.binascii.Error:
        raise ValueError("Invalid base64 encoding")
    except gzip.BadGzipFile:
        raise ValueError("Invalid gzip compression")
    except UnicodeDecodeError:
        raise ValueError("Unable to decode the decompressed data as UTF-8")

def format_json_output(json_str: str, indent: int = 2) -> str:
    """
    Formats JSON string into a human-readable format with improved structure and documentation.
    Args:
        json_str (str): The JSON string to format
        indent (int): Number of spaces for indentation (default: 2)
    Returns:
        str: A formatted, human-readable string explaining the JSON content
    """
    try:
        # Parse the JSON data
        data = json.loads(json_str)
        
        # Create a readable summary
        output = []
        output.append("Workshop Chat Configuration Summary")
        output.append("================================")
        output.append("")
        
        # Workshop type and name
        output.append(f"Workshop Type: {data['type']}")
        output.append(f"Workshop Name: {data['name']}")
        output.append("")
        
        # Format messages
        output.append("System Messages:")
        output.append("---------------")
        for msg in data['messages']:
            if msg['type'] == 'system':
                # Split the text into paragraphs for better readability
                paragraphs = msg['text'].split('\n\n')
                for para in paragraphs:
                    output.append(para.strip())
                    output.append("")
        
        # Format available models
        output.append("Available Models:")
        output.append("----------------")
        for model in data['models']:
            output.append(f"- {model['name']} (ID: {model['id']})")
        
        return "\n".join(output)
        
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format - {str(e)}"
    except KeyError as e:
        return f"Error: Missing expected key in JSON structure - {str(e)}"


def main():
    if len(sys.argv) > 1:
        compressed_string = sys.argv[1]
    else:
        compressed_string = "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"
    
    try:
        decoded_prompt = decode_compressed_prompt(compressed_string)
        print(decoded_prompt)

        print(format_json_output(decoded_prompt))
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    
