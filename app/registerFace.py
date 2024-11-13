import face_recognition
from flask_cors import CORS

FRONTAL = 1
ESQUERDA = 2
DIREITA = 3
CIMA = 4
BAIXO = 5


def get_face_landmarks(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    if len(face_landmarks_list) == 0:
        return None
    return face_landmarks_list[0]
    

def validate_face_position(landmarks, expected_position):
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    nose = landmarks['nose_bridge']

    eye_center_x = (left_eye[0][0] + right_eye[3][0]) / 2
    face_center_x = nose[3][0]

    difference_x = eye_center_x - face_center_x

    left_eye_y = sum([point[1] for point in left_eye]) / len(left_eye)
    right_eye_y = sum([point[1] for point in right_eye]) / len(right_eye)
    eye_center_y = (left_eye_y + right_eye_y) / 2
    face_center_y = nose[len(nose) // 3][1]
    
    difference_y = face_center_y - eye_center_y; 

    if int(expected_position) == FRONTAL:
        if -1 <= difference_x < 3 and 7 <= difference_y <= 10:
            return True, "Cadastro Frontal (Concluido)", 'Rosto na posição correta (Frontal)!'
        elif difference_x < -1:
            return False, "Cadastro Frontal", "Vire um pouco mais para esquerda."
        elif difference_x > 3:
            return False, "Cadastro Frontal", "Vire um pouco mais para direita."
        elif difference_y < 7:
            return False, "Cadastro Frontal", "Vire um pouco mais o rosto para baixo."
        elif difference_y > 10:
            return False, "Cadastro Frontal", "Vire um pouco mais o rosto para cima."
        else:
            return False, "Cadastro Frontal", "Ajuste seu rosto para o centro."

    elif int(expected_position) == ESQUERDA:
        if 20 > difference_x > 10:
            return True, "Cadastro para Esquerda (Concluido)", 'Rosto na posição correta (Esquerda)!'
        elif 5 < difference_x <= 10:
            return False, "Cadastro para Esquerda", "Você está quase lá! Vire um pouco mais para a esquerda."
        elif difference_x > 20:
            return False, "Cadastro para Esquerda", "Você está quase lá! Vire um pouco para a direita."
        else:
            return False, "Cadastro para Esquerda", "Vire um pouco mais o rosto para a esquerda."

    elif int(expected_position) == DIREITA:
        if -20 < difference_x < -10:
            return True, "Cadastro para Direita (Concluido)", 'Rosto na posição correta (Direita)!'
        elif -10 <= difference_x < -5:
            return False, "Cadastro para Direita", "Você está quase lá! Vire um pouco mais para a direita."
        elif difference_x < -20:
            return False, "Cadastro para Direita", "Você está quase lá! Vire um pouco para a esquerda."
        else:
            return False, "Cadastro para Direita", "Vire um pouco mais o rosto para a direita."

    elif int(expected_position) == CIMA:
        if -5 < difference_y < -3:
            return True, "Cadastro para Cima (Concluido)", 'Rosto na posição correta (Cima)!'
        elif difference_y > -3:
            return False, "Cadastro para Cima", "Você está quase lá! Vire um pouco mais para cima. "
        elif difference_y < -5:
            return False, "Cadastro para Cima", "Você está quase lá! Vire um pouco para Baixo. "
        else:
            return False, "Cadastro para Cima", "Vire um pouco mais o rosto para cima."
        
    elif int(expected_position) == BAIXO:
        if  20 > difference_y > 15:
            return True, "Cadastro para Baixo (Concluido)", 'Rosto na posição correta (Baixo)!'
        elif difference_y < 15:
            return False, "Cadastro para Baixo", "Você está quase lá! Vire um pouco mais para baixo."
        elif difference_y > 20:
            return False, "Cadastro para Baixo", "Você está quase lá! Vire um pouco para Cima."
        else:
            return False, "Cadastro para Baixo", "Vire um pouco mais o rosto para baixo."
    return False, "Posição do rosto incorreta.", "Posição do rosto incorreta."
