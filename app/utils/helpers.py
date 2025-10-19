import socket
import psutil
import subprocess
import requests
import config
import os

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

def get_session_token():
    try:
        res = requests.post(
            f"https://{config.SERVER_IP}/login",
            data={"email": config.ROBOCAT_USER, "password": config.ROBOCAT_PASSWORD}
        )
        if res.ok:
            print("🔓 Login correcte del Robocat.")
            return res.cookies.get("session")
        else:
            print(f"❌ Error al fer login del Robocat: {res.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error en la connexió de login: {e}")
        return None

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

def parse_throttled_state(hex_string):
    if '=' in hex_string:
        hex_value = int(hex_string.split('=')[1], 16)
    else:
        hex_value = int(hex_string, 16)

    def is_bit_set(value, bit):
        return (value & (1 << bit)) != 0

    state = {
        "under_voltage_now": is_bit_set(hex_value, 0),
        "frequency_capped_now": is_bit_set(hex_value, 1),
        "throttling_now": is_bit_set(hex_value, 2),
        "under_voltage_occurred": is_bit_set(hex_value, 16),
        "frequency_capped_occurred": is_bit_set(hex_value, 17),
        "throttling_occurred": is_bit_set(hex_value, 18),
    }
    return state

"""def print_throttled_status(status):
    for key, value in status.items():
        emoji = "🟢" if not value else "🔴"
        print(f"{emoji} {key.replace('_', ' ').capitalize()}: {'YES' if value else 'NO'}")
"""

import unicodedata

def normalize_emocions(emocions: list[str]) -> list[str]:
    """
    Normalitza les etiquetes d'emocions retornades per Gemini o altres models.
    Converteix variants, sinònims i faltes d'ortografia a un conjunt canònic.
    """
    # Diccionari de variants conegudes
    mapping = {
        "happy": ["happy", "felic", "feliz", "content", "alegre"],
        "angry": ["angry", "enfadat", "rabia", "furios", "enojat", "irritat"],
        "sad": ["sad", "trist", "depressiu", "deprimit"],
        "surprised": ["surprised", "sorpres", "sorpresa", "astorat", "impactat"],
        "scared": ["scared", "por", "espantat", "atemorit", "temor"],
        "disgusted": ["disgusted", "fastig", "asco", "asquejat", "repulsio"],
        "sleepy": ["sleepy", "adormit", "cansat", "son", "fatigat", "esgotat"],
        "default": ["neutral", "neutralitat", "netral", "sense emocio", "cap emocio", "calmat", "tranquil"],
    }

    resultat = set()

    for emo in emocions:
        # Normalitza accents i caràcters
        e = (
            unicodedata.normalize("NFD", emo)
            .encode("ascii", "ignore")
            .decode("utf-8")
            .lower()
            .strip()
        )

        # Si conté frases, agafem paraula clau més forta
        if " " in e:
            parts = [p for p in e.split() if len(p) > 2]
            e = parts[-1] if parts else e

        trobat = False
        for canonic, variants in mapping.items():
            for v in variants:
                if v in e:
                    resultat.add(canonic)
                    trobat = True
                    break
            if trobat:
                break

        if not trobat:
            # Si no s’ha trobat, conserva l’etiqueta neta
            resultat.add(e)

    if not resultat:
        return ["default"]

    # Retornem en ordre fix per estabilitat
    ordre = ["happy", "angry", "sad", "surprised", "scared", "disgusted", "sleepy", "default"]
    return sorted(resultat, key=lambda x: ordre.index(x) if x in ordre else 999)
