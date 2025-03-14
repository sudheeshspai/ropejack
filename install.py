import os
import shutil
import subprocess
import sys

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root")
        sys.exit(1)

def main():
    check_root()
    termux_bin_path = "/data/data/com.termux/files/usr/bin"
    termux_unknown_path = "/data/data/com.termux/files/usr/unknown"
    usr_bin_path = "/usr/bin"
    usr_unknown_path = "/usr/unknown"
    if os.path.isdir(termux_bin_path):
        shutil.copy("bin/unknown", termux_bin_path)
        os.chmod(os.path.join(termux_bin_path, "unknown"), 0o755)
        os.makedirs(termux_unknown_path, exist_ok=True)
        shutil.copy("bin/index.html", termux_unknown_path)
    elif os.path.isdir(usr_bin_path):
        shutil.copy("bin/unknown", usr_bin_path)
        os.chmod(os.path.join(usr_bin_path, "unknown"), 0o755)
        os.makedirs(usr_unknown_path, exist_ok=True)
        shutil.copy("bin/index.html", usr_unknown_path)
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "localrun"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vulheader"])

if __name__ == "__main__":
    main()
