from pyngrok import ngrok
import requests
import time
import os

def setup_public_access(auth_token=None, region="eu"):
    """Setup ngrok tunnel for public access to local server"""
    
    print("🌐 Setting up public access...")
    
    # Get auth token from environment variable if not provided
    if auth_token is None:
        auth_token = os.getenv('NGROK_AUTH_TOKEN')
        if not auth_token:
            print("❌ No ngrok auth token found!")
            return None
    
    # Check if local server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Local server is not running! Start it first with: python local_server.py")
            return None
    except:
        print("❌ Local server is not running! Start it first with: python local_server.py")
        return None
    
    try:
        # Kill any existing tunnels
        ngrok.kill()
        
        # Set auth token
        ngrok.set_auth_token(auth_token)
        
        # Create tunnel
        public_url = ngrok.connect(8000)
        public_url_str = str(public_url)
        
        print(f"✅ Public tunnel created!")
        print(f"🔗 Public URL: {public_url_str}")
        print(f"📚 Public API Docs: {public_url_str}/docs")
        print(f"🏠 Local URL: http://localhost:8000")
        
        # Test the public URL
        try:
            test_response = requests.get(f"{public_url_str}/health", timeout=10)
            if test_response.status_code == 200:
                print("✅ Public URL is working!")
            else:
                print("⚠️  Public URL might not be ready yet...")
        except:
            print("⚠️  Testing public URL failed, but tunnel should work...")
        
        return public_url_str
        
    except Exception as e:
        print(f"❌ Failed to setup ngrok: {e}")
        return None

def stop_public_access():
    """Stop ngrok tunnels"""
    ngrok.kill()
    print("✅ Public access stopped")

if __name__ == "__main__":
    print("🚀 Ngrok Setup for Local FastAPI Server")
    print("=" * 40)
    
    public_url = setup_public_access()
    
    if public_url:
        print(f"\n💡 Your server is now accessible worldwide!")
        print(f"📱 Share this URL: {public_url}")
        print(f"\n⚠️  Keep this script running to maintain the tunnel")
        print("   Press Ctrl+C to stop the tunnel")
        
        try:
            # Keep the tunnel alive
            while True:
                time.sleep(60)
                print("🔄 Tunnel is active...")
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
            stop_public_access()
    else:
        print("❌ Failed to setup public access") 