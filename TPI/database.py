import face_recognition
import os
import pickle

encodings_db = {}

for filename in os.listdir("empleados"):
    if filename.endswith(".jpg"):
        path = os.path.join("empleados", filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            name = os.path.splitext(filename)[0]
            encodings_db[name] = encodings[0]
        else:
            print(f"No se encontró rostro en {filename}")

# Guardar los embeddings en un archivo
with open("db_encodings.pkl", "wb") as f:
    pickle.dump(encodings_db, f)
