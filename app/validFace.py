import face_recognition
import requests
from io import BytesIO
import cv2 
import numpy as np
import base64

def load_image_from_url(url):
    response = requests.get(url)
    image = face_recognition.load_image_file(BytesIO(response.content))
    return image

def load_image_from_file(file):
    image = face_recognition.load_image_file(file)
    return image

def load_image_from_base64(base64_str):
    base64_str = base64_str.split(",")[1]
    image_data = base64.b64decode(base64_str)
    return face_recognition.load_image_file(BytesIO(image_data))


def validate_face_process(data):
    reference_image_urls = data.get('image_url_ref')
    if not reference_image_urls:
        return {"success": False, "message": "Nenhuma imagem de referência fornecida."}

    known_face_encodings = []
    for image_url in reference_image_urls:
        try:
            known_image = load_image_from_url(image_url)
            face_encodings = face_recognition.face_encodings(known_image)
            if face_encodings:
                known_face_encodings.append(face_encodings[0])
            else:
                reference_image_urls.remove(image_url)
        except Exception as e:
            print('erro no processo')
            return {"success": False, "message": f"Erro ao processar a imagem: {image_url}. Detalhes: {str(e)}"}

    file_data = data.get('image_url')
    if not file_data:
        print('sem ft')
        return {"success": False, "message": "Nenhuma imagem para validar foi fornecida."}

    image = load_image_from_base64(file_data)

    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        print('sem rosto medo')
        return {"success": False, "message": "Nenhum rosto encontrado na imagem para validação."}

    distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
    average_distance = np.mean(distances)
    similarity_percentage = (1 - average_distance) * 100
    acceptance_threshold = 70.0

    if similarity_percentage >= acceptance_threshold:
        return {"success": True, "message": "Rosto validado com sucesso."}
    else:
        return {"success": False, "message": "Rosto invalido."}



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')