# !pip install fastapi uvicorn pyngrok


from fastapi import FastAPI
from pyngrok import ngrok
import uvicorn
import threading
from fastapi import Request
import time
import os

try:
    # Find the process ID (PID) listening on port 8000
    lsof_output = os.popen('lsof -i :8000 -t').read().strip()
    if lsof_output:
        # Kill the process
        os.system(f'kill -9 {lsof_output}')
        print(f"Killed process listening on port 8000: {lsof_output}")
    else:
        print("No process found listening on port 8000.")
except Exception as e:
    print(f"Error during process kill attempt: {e}")

# Add a delay to ensure the process has time to terminate
time.sleep(5)


# Now, call ngrok.kill() for good measure, in case the above didn't catch everything
ngrok.kill()
time.sleep(5)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Colab"}

@app.post("/execute_code")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    
    # Create a restricted globals environment
    restricted_globals = {
        "__builtins__": __builtins__,
        "__name__": "__main__",
        "__doc__": None,
        "__package__": None,
    }
    
    local_vars = {}
    
    try:
        exec(code, restricted_globals, local_vars)
        
        # Comprehensive serialization filter
        def make_serializable(obj, max_depth=3, current_depth=0):
            if current_depth > max_depth:
                return f"<Max depth reached: {type(obj).__name__}>"
            
            try:
                # Test basic JSON serialization
                import json
                json.dumps(obj)
                return obj
            except (TypeError, ValueError, OverflowError):
                pass
            
            # Handle different types
            import types
            import numpy as np
            
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, (types.ModuleType, type)):
                return f"<{type(obj).__name__}: {obj}>"
            elif hasattr(obj, '__dict__'):
                try:
                    return {k: make_serializable(v, max_depth, current_depth + 1) 
                           for k, v in obj.__dict__.items()}
                except:
                    return f"<Object: {type(obj).__name__}>"
            elif isinstance(obj, (list, tuple)):
                try:
                    return [make_serializable(item, max_depth, current_depth + 1) for item in obj]
                except:
                    return f"<Sequence: {type(obj).__name__} with {len(obj)} items>"
            elif isinstance(obj, dict):
                try:
                    return {str(k): make_serializable(v, max_depth, current_depth + 1) 
                           for k, v in obj.items()}
                except:
                    return f"<Dict: {len(obj)} items>"
            else:
                return f"<{type(obj).__name__}: {str(obj)[:100]}>"
        
        serializable_vars = {}
        for key, value in local_vars.items():
            serializable_vars[key] = make_serializable(value)
        
        return {"output": serializable_vars}
        
    except Exception as e:
        return {"output": {"error": str(e), "type": type(e).__name__}}


def run():
    # The reload=True flag can sometimes cause issues in notebooks with multiple runs,
    # so it's generally better to avoid it unless specifically needed for development.
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) # Avoid reload=True in this context
    uvicorn.run(app, host="0.0.0.0", port=8000)

# **Add this line to authenticate ngrok with your authtoken**
# Replace "YOUR_AUTHTOKEN" with your actual authtoken
ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")

# Kill any existing ngrok tunnels and potentially associated processes like uvicorn
# Placing this here ensures a cleaner state before attempting to start the server again.
# !pkill ngrok


# Start ngrok tunnel
public_url = ngrok.connect(8000)
print("Public URL:", public_url)

# Run FastAPI in a separate thread
thread = threading.Thread(target=run)
thread.start()

# Add a small delay to allow the FastAPI app to start
time.sleep(5) # Adjust the sleep duration if necessary

print("FastAPI app should be running now.")



####################Test SERVER#########
import requests
try:
    response = requests.post("https://fd14-154-64-226-166.ngrok-free.app/execute_code", json={"code": "import math \nb=math.sqrt(16)"})
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error accessing endpoint: {e}")
#########################################################