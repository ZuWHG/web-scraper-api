from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/fetchContent', methods=['GET'])
def fetch_content():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title and text content
        title = soup.title.string if soup.title else "No title found"
        paragraphs = [p.text for p in soup.find_all('p')]

        return jsonify({
            "title": title,
            "content": "\n".join(paragraphs[:10])  # Limit to first 10 paragraphs
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
