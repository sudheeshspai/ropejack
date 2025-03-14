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
    termux_ropejack_path = "/data/data/com.termux/files/usr/ropejack"
    usr_bin_path = "/usr/bin"
    usr_ropejack_path = "/usr/ropejack"
    if os.path.isdir(termux_bin_path):
        shutil.copy("bin/ropejack", termux_bin_path)
        os.chmod(os.path.join(termux_bin_path, "ropejack"), 0o755)
        os.makedirs(termux_ropejack_path, exist_ok=True)
        shutil.copy("bin/index.html", termux_ropejack_path)
    elif os.path.isdir(usr_bin_path):
        shutil.copy("bin/ropejack", usr_bin_path)
        os.chmod(os.path.join(usr_bin_path, "ropejack"), 0o755)
        os.makedirs(usr_ropejack_path, exist_ok=True)
        shutil.copy("bin/index.html", usr_ropejack_path)
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "localrun"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vulheader"])

if __name__ == "__main__":
    main()
