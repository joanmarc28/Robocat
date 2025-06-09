import numpy as np
import cv2

## PROCES DE CALIBRATGE DE CAMERA
checkerboard = (8,6)
criteri = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
#para quan: max iter = 30, canvi entre iter > 0.001

obj3DPoints= np.zeros((checkerboard[0]*checkerboard[1], 3), np.float32) #coords x,y,z per cada punt
obj3DPoints[:,:2] = np.mgrid[0:checkerboard[0], 0:checkerboard[1]].T.reshape(-1,2) #converteix en llista de parells [x,y], [x,y]...
# deixa z = 0 (no l'agafa!)

objPoints = []
imgPoints = []

for idx in range(1, 10):
    filepath = f"app/sensors/calibrate/img{idx}.jpg"
    print(f"Cargando {filepath}")
    im = cv2.imread(filepath)
    if im is None:
        print(f"No s'ha pogut carregar la imatge {filepath}!")
        continue

    im_bw = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, cantons = cv2.findChessboardCorners(im_bw, checkerboard, None)

    if ret:
        objPoints.append(obj3DPoints)
        cantons_improved = cv2.cornerSubPix(im_bw, cantons, (11, 11), (-1, -1), criteri)
        imgPoints.append(cantons_improved)
        cv2.drawChessboardCorners(im, checkerboard, cantons_improved, ret)
        cv2.imshow("calibracio_img", im)
        cv2.waitKey(2000)
    else:
        print(f"No s'han trobat cantonades a {filepath}")

cv2.destroyAllWindows()

#a partir d'aqui s'ha de fer proves amb la camera del robot per guardar configs
if len(objPoints) > 0 and len(imgPoints) > 0:
    ret, camera_matrix, distorsion, rot, trans = cv2.calibrateCamera(objPoints, imgPoints, im_bw.shape[::-1], None, None)
    file = cv2.FileStorage("app/sensors/calibrate/camera_calibration.yaml", cv2.FILE_STORAGE_WRITE) 
    file.write("camera_matrix", camera_matrix)
    file.write("distorsion_coef", distorsion) #rot y trans no calen!
    file.release()
    print("S'han guardat les configuracions a camera_calibration.yaml")


