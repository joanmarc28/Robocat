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
