# RopeJack 🔐

> A specialized web-based security toolkit for identifying clickjacking vulnerabilities, enumerating subdomains, and performing bulk security audits.

---

## Features

| Feature | Description |
|---|---|
| 🎯 **Clickjack Scanner** | Checks if a site is missing `X-Frame-Options` or `CSP frame-ancestors` headers |
| 🌐 **Subdomain Finder** | DNS brute-force enumeration using a built-in wordlist — no external API |
| 📋 **Bulk Scanner** | Upload a TXT/PDF file of URLs and scan them all with a live terminal UI |
| 📄 **PDF & TXT Reports** | Export results as a styled PDF or plain TXT file |

---

## Installation

### Requirements
- Python 3.x
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/sudheeshspai/ropejack
cd ropejack

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install flask vulheader requests

# 4. Run the app
cd code
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Usage

### 🎯 Clickjack Scanner (`/`)

1. Enter a URL (e.g. `https://example.com` or just `example.com`)
2. Click **[ SCAN ]**
3. Results show:
   - **VULNERABLE** — lists every missing security header with a fix and MDN reference link
   - **SECURE** — shows which headers are present and their values

**Headers checked:**
- `X-Frame-Options` — prevents the page from being embedded in an iframe
- `Content-Security-Policy: frame-ancestors` — modern replacement for X-Frame-Options

---

### 🌐 Subdomain Finder (`/subdomains`)

1. Enter a domain (e.g. `example.com`)
2. Click **[ SEARCH ]**
3. The tool brute-forces ~200 common subdomain prefixes via DNS resolution
4. Found subdomains are shown with their resolved IP addresses
5. Download results as **TXT** or **PDF**

> Works fully offline — no dependency on crt.sh or any external API.

---

### 📋 Bulk Clickjack Scanner (`/bulkscan`)

1. Upload a **TXT file** with one URL per line (or mixed content — URLs will be extracted automatically)
2. Click **[ START BULK SCAN ]**
3. Watch the live terminal as each URL is checked one by one
4. Results panel on the right shows:
   - **Vulnerable** sites with missing headers listed
   - **Secure** sites that are protected
5. After the scan, download a full **PDF Report** or **TXT Report**

**TXT file format example:**
```
https://example.com
https://target.org
another-site.net
```

---

## Project Structure

```
ropejack/
├── bin/
│   ├── ropejack          # CLI tool (standalone)
│   └── index.html        # HTML used by CLI localrun server
├── code/
│   ├── app.py            # Flask web application
│   └── templates/
│       ├── index.html    # Clickjack scanner page
│       ├── subdomains.html  # Subdomain finder page
│       ├── bulkscan.html    # Bulk scanner page
│       └── clickjack.html   # Clickjack demo page
├── install.py            # System-wide installer (requires sudo)
├── ropejack.py           # Entry point
└── README.md
```

---

## CLI Usage (Optional)

The `bin/ropejack` script can also be used directly from the terminal:

```bash
# Install system-wide (requires root)
sudo python install.py

# Run CLI
ropejack
```

It will prompt for a URL, check the `X-Frame-Options` header, and save vulnerable URLs to `~/vulnerable_urls.txt`.

---

## Tech Stack

- **Backend:** Python 3, Flask, Requests
- **Frontend:** Vanilla HTML/CSS/JS (no frameworks)
- **PDF Export:** jsPDF (client-side)
- **PDF Parsing:** PDF.js (client-side)
- **Subdomain DNS:** Python `socket` + `concurrent.futures`

---

## Credits

- Tool by [Sudheesh](https://github.com/sudheeshspai)
- Contributed by [MrFidal](https://github.com/mrfidal)

---

## Disclaimer

> This tool is intended for **educational and authorized security testing purposes only**.  
> Do not scan websites without explicit permission from the owner.  
> The authors are not responsible for any misuse of this tool.

---

© 2025 RopeJack. All rights reserved.
