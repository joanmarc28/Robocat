import socket
import psutil
import subprocess

# Comrpovar conexio a internet
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

# Obtenir us de la CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Obtenir us de la RAM
def get_ram():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }

# Obtenir problemes de Sobreescalfament, baix voltatge o alt voltatge
def get_throttled_status():
    output = subprocess.check_output(['vcgencmd', 'get_throttled']).decode()
    return output.strip()

# Obtenir temperatura CPU
def get_cpu_temp():
    output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
    return float(output.replace("temp=", "").replace("'C\n", ""))

 # Obtenir frequencia CPU
def get_cpu_freq():
    output = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode()
    return int(output.split('=')[1]) / 1_000_000  # en MHz
