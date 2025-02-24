#!/usr/bin/python3
import vulheader

url = input("Enter the URL to check : ")

result = vulheader.check(url, "Strict-Transport-Security")

if result == "missing":
    print("Strict-Transport-Security: Missing")
    print("Clickjacking risk: Possible. The site might be vulnerable to clickjacking.")
else:
    print("Strict-Transport-Security: Present")
    print("Clickjacking risk: Low. The site is more secure, but still ensure proper 'X-Frame-Options' are in place.")
