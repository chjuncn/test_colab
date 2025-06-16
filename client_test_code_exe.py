import requests
from code_text.code import complex_code6, complex_code7
import time 


base_url = "https://6bd2-89-213-179-161.ngrok-free.app"


codes = [complex_code6, complex_code7]

def test_code(code):
    try:
        response = requests.post(f"{base_url}/execute_code", json={"code": code, "parameters": {"csv_file_path": "vp_ai_app_data.csv"}})
        print("✅ Successfully executed code")
        print(response.json())
        print("="*50)
    except requests.exceptions.RequestException as e:
        print("❌!!!Failed to execute code!!!")

for code in codes:
    test_code(code)
    time.sleep(1)