import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import pickle
import time
from datetime import datetime
import csv

# Cargar base de datos de encodings
with open("db_encodings.pkl", "rb") as f:
    encodings_db = pickle.load(f)

# Inicializar MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Abrir cámara
video_capture = cv2.VideoCapture(0)
roi_width, roi_height = 250, 250

reconocido = False
tiempo_reconocimiento = None

# Variables para liveness (detección de parpadeo)
EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0
BLINKED = False

# Variables para segunda prueba de vida
verificando_liveness_extra = False
inicio_verificacion = None
sonrisa_detectada = False
movimiento_detectado = False

def guardar_log(nombre):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_asistencia.csv", mode="a", newline="") as archivo_log:
        escritor_csv = csv.writer(archivo_log)
        escritor_csv.writerow([nombre, fecha_hora])
    print(f"[LOG] Registro guardado: {nombre} - {fecha_hora}")

def eye_aspect_ratio(landmarks, eye_indices):
    p1 = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    p2 = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    p3 = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    p4 = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    p5 = np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y])
    p6 = np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])

    vertical1 = np.linalg.norm(p2 - p6)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)

    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

def detectar_sonrisa(landmarks):
    izquierda = np.array([landmarks[61].x, landmarks[61].y])
    derecha = np.array([landmarks[291].x, landmarks[291].y])
    inferior = np.array([landmarks[17].x, landmarks[17].y])

    ancho_boca = np.linalg.norm(derecha - izquierda)
    altura_boca = np.linalg.norm(inferior - ((izquierda + derecha) / 2))

    razon_sonrisa = altura_boca / ancho_boca
    return razon_sonrisa > 0.3

def mover_cabeza_lateral(landmarks):
    nariz = landmarks[1].x
    return nariz < 0.45 or nariz > 0.55

# Índices de los ojos en MediaPipe Face Mesh
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    x1 = w // 2 - roi_width // 2
    y1 = h // 2 - roi_height // 2
    x2 = x1 + roi_width
    y2 = y1 + roi_height

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    roi = frame[y1:y2, x1:x2]
    roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

    results = face_detection.process(roi_rgb)
    mesh_results = face_mesh.process(roi_rgb)

    name = "Desconocido"
    color = (0, 0, 255)

    if mesh_results.multi_face_landmarks:
        landmarks = mesh_results.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE_IDX)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE_IDX)
        ear = (left_ear + right_ear) / 2.0

        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                BLINKED = True
            COUNTER = 0

    if results.detections and BLINKED and not verificando_liveness_extra:
        verificando_liveness_extra = True
        inicio_verificacion = time.time()
        print("[INFO] Parpadeo detectado. Esperando sonrisa o movimiento de cabeza...")

    if verificando_liveness_extra:
        if mesh_results.multi_face_landmarks:
            landmarks = mesh_results.multi_face_landmarks[0].landmark

            if detectar_sonrisa(landmarks):
                sonrisa_detectada = True
                print("[INFO] Sonrisa detectada.")

            if mover_cabeza_lateral(landmarks):
                movimiento_detectado = True
                print("[INFO] Movimiento lateral detectado.")

        if sonrisa_detectada or movimiento_detectado:
            face_locations = face_recognition.face_locations(roi_rgb)
            face_encodings = face_recognition.face_encodings(roi_rgb, face_locations)

            if face_encodings:
                encoding = face_encodings[0]
                matches = face_recognition.compare_faces(list(encodings_db.values()), encoding, tolerance=0.5)
                distances = face_recognition.face_distance(list(encodings_db.values()), encoding)

                if True in matches:
                    best_match_index = distances.argmin()
                    name = list(encodings_db.keys())[best_match_index]
                    color = (0, 255, 0)

                if not reconocido and name != "Desconocido":
                    reconocido = True
                    tiempo_reconocimiento = time.time()
                    guardar_log(name)

            verificando_liveness_extra = False
            BLINKED = False
            sonrisa_detectada = False
            movimiento_detectado = False

        elif time.time() - inicio_verificacion > 5:
            print("[WARN] No se detectó gesto adicional dentro del tiempo.")
            verificando_liveness_extra = False
            BLINKED = False
            COUNTER = 0

    cv2.putText(frame, f"Empleado: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    estado_extra = "Parpadeo detectado. Esperando sonrisa o movimiento..." if verificando_liveness_extra else ""
    cv2.putText(frame, estado_extra, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Reconocimiento con Liveness", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if reconocido and (time.time() - tiempo_reconocimiento >= 3):
        break

video_capture.release()
cv2.destroyAllWindows()
