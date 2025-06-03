import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Comprova si hi ha connexió a Internet.
    Per defecte intenta accedir al DNS de Google (8.8.8.8).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"[ERROR] Connexió fallida: {ex}")
        return False

# Obtenir IP local
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
