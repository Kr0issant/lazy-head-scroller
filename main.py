import warnings
warnings.filterwarnings("ignore")

import cv2
import numpy as np
from pynput.mouse import Controller
from cvzone.FaceMeshModule import FaceMeshDetector
import math

def get_face_rotation(img, landmarks):
    img_h, img_w, _ = img.shape
    face_2d = []
    key_indices = [1, 152, 226, 350, 78, 308] 
    
    for idx in key_indices:
        x, y = landmarks[idx][0], landmarks[idx][1]
        face_2d.append([x, y])

    face_2d = np.array(face_2d, dtype=np.float64)

    face_3d = np.array([
        [0.0, 0.0, 0.0],            # Nose tip
        [0.0, -330.0, -65.0],       # Chin
        [-225.0, 170.0, -135.0],    # Left eye left corner
        [225.0, 170.0, -135.0],     # Right eye right corner
        [-150.0, -150.0, -125.0],   # Left mouth corner
        [150.0, -150.0, -125.0]     # Right mouth corner
    ], dtype=np.float64)

    focal_length = 1 * img_w
    cam_center = (img_w / 2, img_h / 2)
    camera_matrix = np.array([
        [focal_length, 0, cam_center[0]],
        [0, focal_length, cam_center[1]],
        [0, 0, 1]
    ], dtype=np.float64)
    dist_coeffs = np.zeros((4, 1), dtype=np.float64)

    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    if success:
        rmat = cv2.Rodrigues(rot_vec)[0]

        pitch = math.atan2(-rmat[2, 0], math.sqrt(rmat[0, 0]**2 + rmat[1, 0]**2))
        yaw = math.atan2(rmat[1, 0] / math.cos(pitch), rmat[0, 0] / math.cos(pitch))
        roll = math.atan2(rmat[2, 1] / math.cos(pitch), rmat[2, 2] / math.cos(pitch))

        pitch = math.degrees(pitch) + 180
        yaw = math.degrees(yaw) + 180
        roll = math.degrees(roll) + 180
        
        return pitch, yaw, roll, face_2d[0]
    else:
        return None, None, None, None

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    CALIBERATION_TIME = 120
    rotations = [[], [], []]
    c_rotations = (0, 0, 0)
    ci = 0

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detector = FaceMeshDetector(maxFaces=1)
    
    mouse = Controller()

    print("""
 _   _                _   _____                _ _           
| | | |              | | /  ___|              | | |          
| |_| | ___  __ _  __| | \ `--.  ___ _ __ ___ | | | ___ _ __ 
|  _  |/ _ \/ _` |/ _` |  `--. \/ __| '__/ _ \| | |/ _ \ '__|
| | | |  __/ (_| | (_| | /\__/ / (__| | | (_) | | |  __/ |   
\_| |_/\___|\__,_|\__,_| \____/ \___|_|  \___/|_|_|\___|_|   
          \n\nCaliberating facial orientation. Please keep your head steady and towards the screen...\n\n""")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            landmarks = faces[0]
            
            pitch, yaw, roll, nose_tip = get_face_rotation(img, landmarks)

            if pitch is not None:
                cv2.putText(img, f'Pitch: {pitch:.2f}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.putText(img, f'Yaw: {yaw:.2f}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.putText(img, f'Roll: {roll:.2f}', (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                if ci < CALIBERATION_TIME:
                    rotations[0].append(pitch)
                    rotations[1].append(yaw)
                    rotations[2].append(roll)
                    ci += 1
                elif ci == CALIBERATION_TIME:
                    c_rotations = (sum(rotations[0]) / 120, sum(rotations[1]) / 120, sum(rotations[2]) / 120)
                    print(f"Caliberated Pitch: {c_rotations[0]:.2f}")
                    print(f"Caliberated Yaw: {c_rotations[1]:.2f}")
                    print(f"Caliberated Roll: {c_rotations[2]:.2f}")
                    ci += 1
                else:
                    if roll - c_rotations[2] < -10 or roll - c_rotations[2] > 300:
                        # print("Up")
                        mouse.scroll(0, 0.3)
                    elif roll - c_rotations[2] > 10:
                        # print("Down")
                        mouse.scroll(0, -0.3)

        # cv2.imshow("Face Rotation", img)  # Only enable if you want to see your face

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()