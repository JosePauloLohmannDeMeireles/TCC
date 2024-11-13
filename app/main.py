from flask import Flask, request, jsonify
import cv2 
import numpy as np
from flask_cors import CORS
import base64
import threading
import time
import validFace as vf 
import registerFace as rf


app = Flask(__name__)
CORS(app)


@app.route('/validate_face', methods=['POST'])
def validate_face():
    data = request.get_json()
    result = None
    timeout_error = {"success": False, "message": "Tempo de processamento excedido."}

    def run_validation():
        nonlocal result
        result = vf.validate_face_process(data)

    validation_thread = threading.Thread(target=run_validation)
    validation_thread.start()
    validation_thread.join(timeout=10)

    if result is None:
        return jsonify(timeout_error)

    return jsonify(result)


@app.route('/criar_face', methods=['POST'])
def criar_face():
    data = request.json['image']
    position = request.json['position']
    
    header, encoded = data.split(",", 1)
    img_data = base64.b64decode(encoded)
    img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

    landmarks = rf.get_face_landmarks(img)
    if landmarks is None:
        return jsonify({"message": "Nenhum rosto detectado.", "valid": False, "suggestions": "Posicione seu rosto no circulo"})

    valid, message, suggestions = rf.validate_face_position(landmarks, position)
    
    return jsonify({"message": message, "valid": valid, "suggestions": suggestions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=False) #mudar debug para true em teste