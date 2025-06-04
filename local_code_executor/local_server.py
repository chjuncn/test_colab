from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import types
import os

app = FastAPI(title="Code Execution Server", version="1.0.0")

# Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {
        "message": "Code Execution Server is running!", 
        "status": "healthy",
        "endpoints": {
            "execute": "/execute_code",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "running", "timestamp": str(os.times())}

@app.post("/execute_code")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    
    if not code.strip():
        return {"output": {"error": "No code provided", "type": "ValueError"}}
    
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
                json.dumps(obj)
                return obj
            except (TypeError, ValueError, OverflowError):
                pass
            
            # Handle NumPy if available
            try:
                import numpy as np
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.bool_):
                    return bool(obj)
            except ImportError:
                pass
            
            # Handle pandas if available
            try:
                import pandas as pd
                if isinstance(obj, pd.DataFrame):
                    return obj.to_dict('records')
                elif isinstance(obj, pd.Series):
                    return obj.to_list()
            except ImportError:
                pass
            
            # Handle other types
            if isinstance(obj, (types.ModuleType, type)):
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
            elif isinstance(obj, set):
                try:
                    return list(obj)
                except:
                    return f"<Set with {len(obj)} items>"
            else:
                return f"<{type(obj).__name__}: {str(obj)[:100]}>"
        
        serializable_vars = {}
        for key, value in local_vars.items():
            serializable_vars[key] = make_serializable(value)
        
        return {"output": serializable_vars, "status": "success"}
        
    except Exception as e:
        return {
            "output": {
                "error": str(e), 
                "type": type(e).__name__,
                "status": "error"
            }
        }

if __name__ == "__main__":
    import sys
    
    print("🚀 Starting Code Execution Server...")
    print("📝 Server will be available at:")
    print("   - Local: http://localhost:8000")
    print("   - Network: http://0.0.0.0:8000") 
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Health Check: http://localhost:8000/health")
    print("\n⚡ Press Ctrl+C to stop the server")
    print("="*50)
    
    try:
        # Start server without reload to avoid the warning
        uvicorn.run(
            "local_server:app",  # Use import string instead of app object
            host="0.0.0.0", 
            port=8000, 
            log_level="info",
            reload=False  # Disable reload to avoid warning
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("💡 Try running on a different port:")
        print("   uvicorn local_server:app --host 0.0.0.0 --port 8001")
        sys.exit(1) 