import os
import shutil
import subprocess
import sys

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root")
        sys.exit(1)

def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        os.chmod(dst, 0o755)
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")
        sys.exit(1)

def main():
    check_root()
    
    termux_bin_path = "/data/data/com.termux/files/usr/bin"
    termux_ropejack_path = "/data/data/com.termux/files/usr/ropejack"
    usr_bin_path = "/usr/bin"
    usr_ropejack_path = "/usr/ropejack"

    if os.path.isdir(termux_bin_path):
        copy_file("bin/ropejack", os.path.join(termux_bin_path, "ropejack"))
        os.makedirs(termux_ropejack_path, exist_ok=True)
        copy_file("bin/index.html", os.path.join(termux_ropejack_path, "index.html"))
    
    elif os.path.isdir(usr_bin_path):
        copy_file("bin/ropejack", os.path.join(usr_bin_path, "ropejack"))
        os.makedirs(usr_ropejack_path, exist_ok=True)
        copy_file("bin/index.html", os.path.join(usr_ropejack_path, "index.html"))
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "localrun"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "vulheader"])
    except subprocess.CalledProcessError as e:
        print(f"Error during pip install: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
