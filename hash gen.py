import os
import hashlib

def generate_hashes(directory, output_file):
    """Generate hashes for all files in a directory and write them to a file."""
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                hash_value = calculate_hash(file_path)
                f.write(f"{file_path},{hash_value}\n")
    print("Hashes generated and saved successfully.")

def calculate_hash(file_path, algorithm='sha256'):
    """Calculate the hash value of a file."""
    hash_function = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_function.update(chunk)
    return hash_function.hexdigest()

# Example usage:
directory_to_hash = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
output_file_path = 'hashes.txt'

generate_hashes(directory_to_hash, output_file_path)
