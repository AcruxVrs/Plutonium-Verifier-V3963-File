import os
import hashlib
import shutil
import requests

def generate_checksum(file_path, algorithm='sha256'):
    """Generate checksum for a file."""
    hash_function = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_function.update(chunk)
    return hash_function.hexdigest()

def download_file(url, output_file_path):
    """Download a file from a URL and save it."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded file from {url} and saved it to {output_file_path}")
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")

def verify_files_with_hashes(main_folder, hash_file_path):
    """Check files in the main folder against the hash values."""
    hashes = read_hashes_from_file(hash_file_path)
    total_verified = len(hashes)

    for file_path, expected_hash in hashes.items():
        file_path = os.path.join(main_folder, file_path)
        if os.path.isfile(file_path):
            calculated_hash = generate_checksum(file_path)
            if calculated_hash == expected_hash:
                print(f"File integrity verified: {file_path}")
                total_verified -= 1
            else:
                print(f"File integrity verification failed: {file_path}")
                print(f"Expected hash: {expected_hash}")
                print(f"Calculated hash: {calculated_hash}")
                # File corrupted, download and replace it
                github_url = construct_github_url(file_path)
                create_missing_directories(file_path)
                download_and_save_file(github_url, file_path)
                total_verified -= 1
        else:
            print(f"File not found: {file_path}")
            # File missing, create directories and then download it from GitHub
            github_url = construct_github_url(file_path)
            create_missing_directories(file_path)
            download_and_save_file(github_url, file_path)
            total_verified -= 1

    print("\nVerification Summary:")
    print(f"Total files verified: {len(hashes)}")
    

def construct_github_url(file_path):
    """Construct GitHub URL for downloading a file based on the relative path."""
    github_repo_url = 'https://raw.githubusercontent.com/AcruxVrs/Plutonium-Verifier/main/PlutoniumCopy%20-%20Copy/'
    relative_path = os.path.relpath(file_path, os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium'))
    return github_repo_url + relative_path.replace('\\', '/')

def read_hashes_from_file(hash_file_path):
    """Read hash values from a file."""
    hashes = {}
    with open(hash_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                file_path, expected_hash = parts
                hashes[file_path] = expected_hash
    return hashes

def create_missing_directories(file_path):
    """Create missing directories for the given file path."""
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    print(f"Created missing directories: {directory}")

def move_file_to_directory(file_path, target_directory):
    """Move a file to the specified directory."""
    shutil.move(file_path, target_directory)

def download_and_save_file(url, output_file_path):
    """Download a file from a URL and save it."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded file from {url} and saved it to {output_file_path}")
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")

# Example usage:
main_folder = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
hash_file_path = 'hashes.txt'

# Verify files with hashes
verify_files_with_hashes(main_folder, hash_file_path)
