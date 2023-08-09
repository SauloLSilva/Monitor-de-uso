import cv2
import time
import os
from datetime import datetime
from app.models.mongodb import Mongodatabase
import subprocess

mongodb = Mongodatabase()

try:
    subprocess.check_output(['sudo', 'service', 'mongod', 'start'])
except:
    pass

def check_face_existente():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    while True:
        # Capturar um frame da webcam
        ret, frame = cap.read()
        
        # Converter o frame para escala de cinza para a detecção do rosto
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar faces no frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            # Borrar o rosto detectado
            blurred_face = cv2.GaussianBlur(frame[y:y+h, x:x+w], (99, 99), 30)
            frame[y:y+h, x:x+w] = blurred_face
        
        # Verificar se pelo menos uma face foi detectada
        if len(faces) > 0:
            return True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def get_logged_in_user():
    #coleta usuário logado
    try:
        cmd = os.popen("who").read()
        usuarios = cmd.strip().split("\n")
        usuario_logado = [usuario.split()[0] for usuario in usuarios]
        return usuario_logado[0]
    except Exception as e:
        pass

def check_uso():
    while True:
        data = datetime.now().strftime('%d-%m-%y')
        try:
            pc_em_uso = check_face_existente()
            if pc_em_uso == True:
                usuario = get_logged_in_user()
                mongodb.get_dados(data, usuario, 5)
                time.sleep(5)
        except Exception as err:
            pass

check_uso()