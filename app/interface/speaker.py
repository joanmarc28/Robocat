import os
import subprocess
import threading
import queue
import random
import config

class Speaker:
    def __init__(self):
        self.sound_queue = queue.Queue()
        self.audio_device = getattr(config, "AUDIO_DEVICE", "plughw:1,0")
        self.thread = None
        self.lock = threading.Lock()

    def _play(self, filename):
        path = os.path.join(config.SOUNDS_DIR, filename)
        if not os.path.exists(path):
            print(f"[ERROR] Sound not found: {path}")
            return
        try:
            subprocess.run(["aplay", "-D", self.audio_device, path], check=True)
        except Exception as e:
            print(f"[ERROR] Failed to play {filename}: {e}")

    def _sound_loop(self):
        while not self.sound_queue.empty():
            filename = self.sound_queue.get()
            self._play(filename)
            self.sound_queue.task_done()
        with self.lock:
            self.thread = None

    def _start_thread_if_needed(self):
        with self.lock:
            if self.thread is None or not self.thread.is_alive():
                self.thread = threading.Thread(target=self._sound_loop, daemon=True)
                self.thread.start()

    def play_sound(self, filename):
        self.sound_queue.put(filename)
        self._start_thread_if_needed()

    def say_emotion(self, emotion):
        if emotion in config.STATES:
            sounds = config.STATES[emotion].get("sounds", [])
            if sounds:
                sound = random.choice(sounds)
                self.play_sound(sound)
            else:
                print(f"[INFO] No sounds listed for emotion: {emotion}")
        else:
            print(f"[INFO] Unknown emotion: {emotion}")
