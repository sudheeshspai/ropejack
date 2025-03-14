#!/usr/bin/python3
import vulheader
import os
import localrun

url = input("Enter the URL to check : ")

result = vulheader.check(url, "Strict-Transport-Security")

if result == "missing":
    print("Strict-Transport-Security: Missing")
    print("Clickjacking risk: Possible. The site might be vulnerable to clickjacking.")
    file_path = os.path.expanduser('~/vulnerable_urls.txt')
    with open(file_path, 'a') as f:
        f.write(f"{url}\n")
    running_address = localrun.run_server('127.0.0.1', 8000, silent=True)
    print(f"Running port is : {running_address}")
else:
    print("Strict-Transport-Security: Present")
    print("Clickjacking risk: Low. The site is more secure, but still ensure proper 'X-Frame-Options' are in place.")
