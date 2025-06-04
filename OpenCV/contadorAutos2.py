import cv2
import numpy as np

# 1. Inicializamos el sustractor de fondo
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
min_contour_area = 8500  # evitar detectar cosas muy pequeñas como autos

# Línea de conteo (horizontal, centrada)
line_position = 510
offset = 20  # margen para detección de cruce

# Para guardar los centroides anteriores y evitar dobles conteos
centroides_previos = []
conteo_autos = 0

# 2. Captura de video (puede ser una cámara o archivo)
cap = cv2.VideoCapture("OpenCV/Cars Moving On Road Stock Footage - Free Download.mp4")  # cambia esto si es cámara

def get_centroid(contour):
    M = cv2.moments(contour)
    if M["m00"] == 0: return None
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Preprocesamiento
    fg_mask = bg_subtractor.apply(frame)

    # 4. Filtrado morfológico (Erosion seguido de Dilation)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

    # 5. Encontramos contornos
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centroides_frame = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            # Polígono para aproximar la forma
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

            # Centroide del polígono
            centroide = get_centroid(contour)
            if centroide:
                cx, cy = centroide
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                centroides_frame.append(centroide)

                # Verificamos si el centroide cruza la línea de conteo
                if (cy > line_position - offset) and (cy < line_position + offset):
                    if all(abs(cx - prev_cx) > 20 or abs(cy - prev_cy) > 20 for prev_cx, prev_cy in centroides_previos):
                        conteo_autos += 1
                        centroides_previos.append((cx, cy))

    # Línea de conteo
    cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (255, 0, 0), 2)
    cv2.putText(frame, f"Autos contados: {conteo_autos}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 50), 2)

    # Mostrar resultados
    cv2.imshow("Video", frame)
    cv2.imshow("Foreground Mask", fg_mask)

    # Salida con tecla ESC
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
