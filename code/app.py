from flask import Flask, request, jsonify, render_template
import json
import os
import vulheader

app = Flask(__name__)

json_file_path = 'urls.json'

def load_urls():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return []

def save_urls(urls):
    with open(json_file_path, 'w') as file:
        json.dump(urls, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_url():
    url = request.form.get('url')
    if url:
        result = vulheader.check(url)
        
        if result == "missing":
            urls = load_urls()
            urls.append(url)
            save_urls(urls)
            return jsonify({"message": "URL saved successfully! It is vulnerable to clickjacking.", "url": url}), 200
        else:
            return jsonify({"message": "URL is secure.", "url": url}), 200
            
    return jsonify({"message": "Invalid URL!"}), 400

@app.route('/clickjack')
def clickjack():
    url = request.args.get('url')
    return render_template('clickjack.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
