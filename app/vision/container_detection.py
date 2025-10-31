from vision.camera import RobotCamera
from ultralytics import YOLO
import os
import pickle
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import logging

PATH = "/home/Robocat/Robocat"
logger = logging.getLogger(__name__)

class ContainerDetection:
    def detect_container(frame, camera=None):
        logger.info("Detectant container...")
        #versio anterior de YOLO -> 8.3.99 (pip install ultralytics==8.3.99)
        model = YOLO(PATH+"/app/assets/yolo/containers_model/weights/YOLO11seg_contenedores_batch1n_1216.pt")
        results = model.predict(frame, save=True, imgsz=416)
        if results:
            for result in results:
                logger.info("Container detectat")
                box = result.boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                if camera is not None:
                    camera.add_overlay_box((x1,y1,x2,y2), label="container")
                container = frame[y1:y2, x1:x2]
                #annotated = results[0].plot()
                #cv2.imwrite("output/result.jpg", annotated)
                return container, (x1,y1, x2, y2)
        else:
            logger.info("No s'ha detectat cap container")
            return None, None
        

        
