import json
import random
import sys

def create_sample_databases(input_file, output_prefix="sample"):
    """
    Read a JSON database and create sample databases with random elements.
    
    Args:
        input_file: Path to the input JSON file
        output_prefix: Prefix for output files (default: "sample")
    """
    # Read the original database
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not a valid JSON file.")
        return
    
    # Verify it's an array
    if not isinstance(data, list):
        print("Error: JSON file must contain an array of objects.")
        return
    
    total_items = len(data)
    print(f"Original database contains {total_items} items.")
    
    # Define sample sizes
    sample_sizes = [50, 100, 200, 500]
    
    # Create each sample database
    for size in sample_sizes:
        if size > total_items:
            print(f"Warning: Cannot create sample of size {size} (only {total_items} items available). Skipping.")
            continue
        
        # Get random sample without replacement
        sample = random.sample(data, size)
        
        # Write to output file
        output_file = f"{output_prefix}_{size}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample, f, indent=2, ensure_ascii=False)
        
        print(f"Created '{output_file}' with {size} random items.")
    
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_json_file> [output_prefix]")
        print("Example: python script.py database.json sample")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else "sample"
    
    create_sample_databases(input_file, output_prefix)