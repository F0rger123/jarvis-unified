#!/usr/bin/env python3
"""
Jarvis Test Script - Diagnose startup issues
"""
import sys
print("Python version:", sys.version)

# Test 1: Basic imports
print("\n[1/5] Testing core imports...")
try:
    import flask
    print(f"✅ Flask: {flask.__version__}")
except Exception as e:
    print(f"❌ Flask: {e}")

try:
    import flask_cors
    print("✅ Flask-CORS")
except Exception as e:
    print(f"❌ Flask-CORS: {e}")

try:
    import requests
    print(f"✅ Requests: {requests.__version__}")
except Exception as e:
    print(f"❌ Requests: {e}")

# Test 2: Jarvis imports
print("\n[2/5] Testing Jarvis imports...")
sys.path.insert(0, '.')
try:
    from core.jarvis import JarvisConfig, Jarvis
    print("✅ core.jarvis")
except Exception as e:
    print(f"❌ core.jarvis: {e}")

try:
    from memory import Memory
    print("✅ memory")
except Exception as e:
    print(f"❌ memory: {e}")

try:
    from api.google_services import GoogleServices
    print("✅ api.google_services")
except Exception as e:
    print(f"❌ api.google_services: {e}")

# Test 3: UI imports
print("\n[3/5] Testing UI imports...")
try:
    from ui.web_ui import JarvisTronUI
    print("✅ ui.web_ui")
except Exception as e:
    print(f"❌ ui.web_ui: {e}")

# Test 4: Config
print("\n[4/5] Testing config...")
try:
    config = JarvisConfig('.env')
    print(f"✅ Config loaded. API key exists: {bool(config.get('gemini_api_key'))}")
except Exception as e:
    print(f"❌ Config: {e}")

# Test 5: Start minimal server
print("\n[5/5] Testing server start...")
try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return 'Jarvis Test OK'
    
    print("✅ Minimal Flask app created")
    print("Testing server on port 5001...")
    
    # Start in background thread
    import threading
    server = threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False))
    server.daemon = True
    server.start()
    
    import time
    time.sleep(2)
    
    # Test with requests
    import urllib.request
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:5001/', timeout=5)
        print(f"✅ Server responding: {resp.read().decode()}")
    except Exception as e:
        print(f"❌ Server not responding: {e}")
    
except Exception as e:
    print(f"❌ Server: {e}")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)