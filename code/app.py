from flask import Flask, request, jsonify, render_template
import json
import os
import socket
import requests
import vulheader
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

json_file_path = 'urls.json'

# ─── Subdomain wordlist ────────────────────────────────────────────────────────
WORDLIST = [
    "www","mail","ftp","smtp","pop","imap","webmail","email","mx","mx1","mx2",
    "ns1","ns2","ns3","ns4","dns","dns1","dns2","relay","smtp1","smtp2",
    "api","api2","api3","rest","graphql","grpc","gateway","proxy",
    "dev","develop","development","staging","stage","stg","test","testing",
    "beta","alpha","demo","sandbox","uat","qa","sit","prod","production","preprod",
    "admin","panel","dashboard","portal","control","manage","management","console",
    "login","auth","sso","oauth","id","identity","account","accounts",
    "app","apps","mobile","m","wap","pwa","web","www2","www3","www1",
    "blog","news","press","media","events","magazine","articles",
    "shop","store","ecommerce","pay","payment","payments","billing","checkout","cart",
    "cdn","static","assets","files","img","images","pics","photos","media","upload",
    "download","backup","archive","data","docs","doc","wiki","kb","help","support",
    "vpn","remote","rdp","ssh","sftp","ftp2","ntp","ldap",
    "db","database","mysql","postgres","postgresql","redis","mongo","mongodb",
    "elasticsearch","elastic","kibana","grafana","prometheus","influxdb",
    "git","gitlab","github","repo","svn","bitbucket","code","source",
    "jenkins","ci","cd","build","deploy","devops","ansible","k8s","kubernetes",
    "monitor","monitoring","status","health","ping","uptime","alert","alerts",
    "forum","community","chat","slack","discord","helpdesk","ticket","tickets",
    "analytics","stats","metrics","tracking","reports","report","bi",
    "internal","intranet","extranet","corp","office","employee","hr",
    "cloud","aws","gcp","azure","s3","storage","bucket","object",
    "v1","v2","v3","old","new","legacy","classic","next",
    "secure","ssl","vpn2","gateway2","firewall","waf","load","lb",
    "crm","erp","jira","confluence","sharepoint","exchange","outlook",
    "zoom","meet","video","stream","live","broadcast",
    "partner","partners","vendor","vendors","client","clients","customer","customers",
    "affiliate","affiliates","reseller","resellers","wholesale",
    "jobs","careers","hr","recruitment","talent",
    "legal","privacy","terms","compliance","security","abuse",
    "api-dev","api-staging","api-prod","api-v1","api-v2",
    "dev-api","staging-api","prod-api","test-api",
    "smtp-relay","mail1","mail2","mail3","pop3","imap4",
    "webdav","caldav","carddav","dav",
    "whm","cpanel","plesk","hosting","server","host",
    "proxy1","proxy2","cache","varnish","nginx","apache",
    "microservice","services","service","worker","queue","broker","kafka",
    "auth0","keycloak","okta","ping","saml",
    "prd","stag","int","ext","local","lan",
]

# ─── Helpers ───────────────────────────────────────────────────────────────────
def load_urls():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            return json.load(f)
    return []

def save_urls(urls):
    with open(json_file_path, 'w') as f:
        json.dump(urls, f)

def resolve_subdomain(subdomain):
    """Try to resolve a subdomain via DNS. Returns (subdomain, ip) or None."""
    try:
        ip = socket.gethostbyname(subdomain)
        return {"subdomain": subdomain, "ip": ip}
    except socket.gaierror:
        return None

# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_url():
    url = request.form.get('url', '').strip()
    if not url:
        return jsonify({"message": "Invalid URL!"}), 400

    # Auto-add scheme if missing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    try:
        resp = requests.get(url, timeout=10, allow_redirects=True,
                            headers={"User-Agent": "Mozilla/5.0 (RopeJack Scanner)"})
        headers = {k.lower(): v for k, v in resp.headers.items()}

        missing = []
        present = []

        xfo = headers.get('x-frame-options')
        csp = headers.get('content-security-policy', '')

        if xfo:
            present.append({"header": "X-Frame-Options", "value": xfo})
        else:
            missing.append({
                "header": "X-Frame-Options",
                "fix": "Add to server config: X-Frame-Options: SAMEORIGIN",
                "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"
            })

        if 'frame-ancestors' in csp:
            present.append({"header": "Content-Security-Policy: frame-ancestors", "value": csp})
        else:
            missing.append({
                "header": "Content-Security-Policy (frame-ancestors)",
                "fix": "Add to server config: Content-Security-Policy: frame-ancestors 'self'",
                "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors"
            })

        if missing:
            urls = load_urls()
            if url not in urls:
                urls.append(url)
                save_urls(urls)
            return jsonify({
                "vulnerable": True,
                "message": "Site is vulnerable to clickjacking!",
                "url": url,
                "missing": missing,
                "present": present
            }), 200
        else:
            return jsonify({
                "vulnerable": False,
                "message": "Site is protected against clickjacking.",
                "url": url,
                "missing": [],
                "present": present
            }), 200

    except requests.exceptions.ConnectionError:
        return jsonify({"vulnerable": False, "message": "Could not connect to the URL.", "url": url, "missing": [], "present": []}), 200
    except requests.exceptions.Timeout:
        return jsonify({"vulnerable": False, "message": "Connection timed out.", "url": url, "missing": [], "present": []}), 200
    except Exception as e:
        return jsonify({"vulnerable": False, "message": f"Error: {str(e)}", "url": url, "missing": [], "present": []}), 200


@app.route('/clickjack')
def clickjack():
    url = request.args.get('url')
    return render_template('clickjack.html', url=url)

@app.route('/subdomains')
def subdomains():
    return render_template('subdomains.html')

@app.route('/bulkscan')
def bulkscan():
    return render_template('bulkscan.html')

@app.route('/bulkscan/parse', methods=['POST'])
def bulkscan_parse():
    """Extract URLs from an uploaded TXT file (PDF handled client-side)."""
    f = request.files.get('file')
    if not f:
        return jsonify({"urls": []}), 400
    text = f.read().decode('utf-8', errors='ignore')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return jsonify({"urls": lines})


@app.route('/subdomains/search')
def subdomains_search():
    domain = request.args.get('domain', '').strip()
    # strip protocol/trailing slash if user pasted a full URL
    domain = domain.replace('https://', '').replace('http://', '').rstrip('/').split('/')[0]

    if not domain:
        return jsonify({"error": "No domain provided."}), 400

    candidates = [f"{word}.{domain}" for word in WORDLIST]
    found = []

    try:
        with ThreadPoolExecutor(max_workers=80) as executor:
            futures = {executor.submit(resolve_subdomain, sub): sub for sub in candidates}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)

        found.sort(key=lambda x: x['subdomain'])
        return jsonify({"subdomains": found, "count": len(found)})

    except Exception as e:
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
