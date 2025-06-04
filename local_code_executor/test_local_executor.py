import requests
import json
import time

# Local server URL
BASE_URL = "http://localhost:8000"

def test_server_connection():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def execute_code(code, description=""):
    """Execute code on the server and return results"""
    if description:
        print(f"\n🧪 Testing: {description}")
        print("-" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute_code",
            json={"code": code},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("✅ SUCCESS")
                output = result.get("output", {})
                if output:
                    print("📤 Output:")
                    for key, value in output.items():
                        print(f"   {key}: {value}")
                else:
                    print("   (No variables created)")
            else:
                print("🔶 EXECUTION ERROR")
                error_info = result.get("output", {})
                print(f"   Error: {error_info.get('error', 'Unknown error')}")
                print(f"   Type: {error_info.get('type', 'Unknown')}")
        else:
            print(f"❌ HTTP ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {e}")

# Test cases
test_cases = [
    # Basic tests
    ("Basic Arithmetic", "result = 2 + 2"),
    
    ("Variable Assignment", """
x = 10
y = 20
sum_result = x + y
product = x * y
"""),
    
    # Import tests
    ("Math Import", """
import math
pi_value = math.pi
sqrt_result = math.sqrt(16)
factorial_5 = math.factorial(5)
"""),
    
    ("Multiple Imports", """
import random
import datetime
from collections import Counter

random.seed(42)
numbers = [random.randint(1, 100) for _ in range(10)]
timestamp = datetime.datetime.now().isoformat()
word_count = Counter(['hello', 'world', 'hello', 'python'])

result = {
    'numbers': numbers,
    'timestamp': timestamp,
    'word_frequencies': dict(word_count)
}
"""),
    
    # Data processing
    ("List Processing", """
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared = [x**2 for x in data]
filtered = [x for x in data if x % 2 == 0]
total = sum(data)

stats = {
    'original': data,
    'squared': squared,
    'even_numbers': filtered,
    'sum': total,
    'average': total / len(data)
}
"""),
    
    # NumPy test (if available)
    ("NumPy Test", """
try:
    import numpy as np
    
    data = np.random.randn(50)
    stats = {
        'mean': float(np.mean(data)),
        'std': float(np.std(data)),
        'min': float(np.min(data)),
        'max': float(np.max(data))
    }
    
    # Create histogram
    hist, bins = np.histogram(data, bins=5)
    histogram = {
        'counts': hist.tolist(),
        'bins': bins.tolist()
    }
    
    result = {
        'stats': stats,
        'histogram': histogram,
        'data_length': len(data)
    }
    
except ImportError:
    result = {'error': 'NumPy not available'}
"""),
    
    # Function and class test
    ("Functions and Classes", """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

calc = Calculator()
sum_result = calc.add(15, 25)
fib_10 = fibonacci(10)

results = {
    'calculator_sum': sum_result,
    'calculator_history': calc.history,
    'fibonacci_10': fib_10
}
""")
]

def main():
    print("🧪 Local FastAPI Server Test Suite")
    print("=" * 50)
    
    # Check server connection
    if not test_server_connection():
        print("\n💡 To start the server, run: python local_server.py")
        return
    
    print(f"\n🔗 Server URL: {BASE_URL}")
    print(f"📚 API Docs: {BASE_URL}/docs")
    
    # Run test cases
    for description, code in test_cases:
        execute_code(code, description)
        time.sleep(0.5)  # Small delay between tests
    
    print(f"\n{'='*50}")
    print("🎉 Test suite completed!")
    print("💡 You can also test manually at: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 