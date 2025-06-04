import requests
from code_text.code import simple_code1, simple_code2, complex_code1, complex_code2, complex_code3, complex_code4, complex_code5
import time 


base_url = "https://fd14-154-64-226-166.ngrok-free.app"


codes = [simple_code1, simple_code2, complex_code1, complex_code2, complex_code3, complex_code4, complex_code5]

def test_code(code):
    try:
        response = requests.post(f"{base_url}/execute_code", json={"code": code})
        print("✅ Successfully executed code")
        print(response.json())
        print("="*50)
    except requests.exceptions.RequestException as e:
        print("❌!!!Failed to execute code!!!")

for code in codes:
    test_code(code)
    time.sleep(1)