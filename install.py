import os
import shutil

def move_and_make_executable(file_path):
    if not os.path.isfile(file_path):
        print("Error: File not found!")
        return
    
    bin_dirs = ["/bin", "/data/data/com.termux/files/usr/bin"]
    file_name = os.path.basename(file_path)
    
    for bin_dir in bin_dirs:
        dest_path = os.path.join(bin_dir, file_name)
        try:
            shutil.move(file_path, dest_path)
            os.chmod(dest_path, 0o755)
            print(f"File moved to {dest_path} and made executable.")
            return
        except PermissionError:
            print(f"Permission denied for {dest_path}! Try running as root (sudo).")
        except Exception as e:
            print(f"An error occurred: {e}")

file_to_move = "unknown"
