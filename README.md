# fb-trap  
A Flask trap server that logs visitor IP, ISP, device info and optional geolocation.  

## Usage  
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 trap_server.py
ngrok http 5000
