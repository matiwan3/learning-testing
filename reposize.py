import os

def get_directory_size(directory):
    total_size = 0
    for path, dirs, files in os.walk(directory):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size

directory = "../learning-testing"
size = get_directory_size(directory)
size_mb = round(size / 1048576, 2)
print(f"Size of {directory}: {size_mb} MB")
