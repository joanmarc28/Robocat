import os
import subprocess

# Directori de sons
SOUNDS_DIR = "assets/sounds_clean"

def play_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    if not os.path.exists(path):
        print(f"[ERROR] Sound not found: {path}")
        return

    try:
        subprocess.run(["aplay", "-D", "plughw:1,0", path], check=True)
    except Exception as e:
        print(f"[ERROR] Failed to play {filename}: {e}")

def play_effect(filename):
    # Només cridem play_sound (igual)
    play_sound(filename)

def say_emotion(emotion):
    mapping = {
        "default": "neutral_1_clean.wav",
        "happy": "cute_1_clean.wav",
        "sad": "sick_1_clean.wav",
        "angry": "angry_1_clean.wav",
        "surprised": "funny_1_clean.wav",
        "sleepy": "angry_2_clean.wav"
    }
    if emotion in mapping:
        play_effect(mapping[emotion])
    else:
        print(f"[INFO] No sound mapped for emotion: {emotion}")
