# 🚀 Test the running server:

```
python client_test_code_exe.py
```
If you get error, check if the server is running by
https://fd14-154-64-226-166.ngrok-free.app/docs#/.

Note: Replace the url to yours if you want to test your own server.

# 🚀 SETUP YOUR OWN Local Code Execution Server

A FastAPI server that executes Python code remotely with public access via ngrok.

## 📋 Prerequisites

- Python 3.7+
- ngrok account (free)

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
pip install fastapi uvicorn pyngrok requests numpy
```

### 2. Get Ngrok Auth Token
1. Sign up at [ngrok.com](https://ngrok.com)
2. Get your auth token from [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

### 3. Set Environment Variable
```bash
export NGROK_AUTH_TOKEN="your_token_here"
```

### 4. Start Server
**Option A: All-in-one (Recommended)**
```bash
caffeinate -i python run_server.py
```

**Option B: Separate terminals**
```bash
# Terminal 1
caffeinate -i python local_server.py

# Terminal 2  
caffeinate -i ngrok http 8000 --region=eu
```

## 🌐 Access Your Server

After starting, you'll get:
- **Local**: `http://localhost:8000`
- **Public**: `https://xxxxx.ngrok-free.app` (shown in terminal)
- **API Docs**: Add `/docs` to either URL

## 🧪 Test It

**Via curl:**
```bash
curl -X POST https://your-ngrok-url.ngrok-free.app/execute_code \
  -H "Content-Type: application/json" \
  -d '{"code": "result = 2 + 2\nprint(result)"}'
```

**Via Python:**
```python
import requests

url = "https://your-ngrok-url.ngrok-free.app/execute_code"
response = requests.post(url, json={"code": "import numpy as np\ndata = np.array([1,2,3])\nresult = data.mean()"})
print(response.json())
```

## 💡 Tips

- **Keep laptop awake**: `caffeinate -i` prevents sleep but allows screen to turn off
- **EU region works best** if US region fails
- **Both server and ngrok must run** for public access
- **Public URL changes** each time you restart ngrok

## 🛑 Stop Server

Press `Ctrl+C` in the terminal running the server.



## ⚠️ Security Note

This server executes arbitrary Python code. Only use in trusted environments.
