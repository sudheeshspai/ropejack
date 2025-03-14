#!/usr/bin/python3
import vulheader
import os

url = input("Enter the URL to check : ")
result = vulheader.check(url, "Strict-Transport-Security")
if result == "missing":
    print("Strict-Transport-Security: Missing")
    print("Clickjacking risk: Possible. The site might be vulnerable to clickjacking.")
    file_path = os.path.expanduser('~/vulnerable_urls.txt')
    with open(file_path, 'a') as f:
        f.write(f"{url}\n")
        print(f"Vulnerable URL saved to {file_path}")
else:
    print("Strict-Transport-Security: Present")
    print("Clickjacking risk: Low. The site is more secure, but still ensure proper 'X-Frame-Options' are in place.")
