import asyncio
import websockets
import cv2
from picamera2 import Picamera2
import io
import config

SERVER_URL = f"wss://{config.SERVER_IP}/ws/stream/" + config.ROBOT_ID  # Canvia pel teu servidor

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# Carrega el detector de cares preentrenat
#face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_smile.xml")

async def send_frames():
    async with websockets.connect(SERVER_URL) as websocket:
        print("📡 Connectat al servidor")
        while True:
            frame = picam2.capture_array()

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, "Cara", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                # Ulls
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    cv2.putText(roi_color, "Ull", (ex, ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # Somriures
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
                    cv2.putText(roi_color, "Somriure", (sx, sy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


            _, jpeg = cv2.imencode(".jpg", frame)
            await websocket.send(jpeg.tobytes())
            await asyncio.sleep(0.03)  # ~30 FPS


