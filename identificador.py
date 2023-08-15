import cv2
from app.models.simple_facerec import SimpleFacerec
import time
import os
from datetime import datetime
from app.models.mongodb import Mongodatabase
import subprocess
from app.models.bot_telegram import Bot_alerta

telegram = Bot_alerta()

mongodb = Mongodatabase()

try:
    subprocess.check_output(['sudo', 'service', 'mongod', 'start'])
except:
    pass

sfr = SimpleFacerec()
sfr.load_encoding_images()

def check_face_existente():


    cap = cv2.VideoCapture(-1)

    while True:
        ret, frame = cap.read()

        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        # cv2.imshow("Frame", frame)
        passagem = ''.join(face_names)
        retorno = passagem.split("_")
        usuario = retorno[0]
        if passagem == 'Unknown':
            return False
        if passagem == '':
            pass
        else:
            return True, usuario

        key = cv2.waitKey(1)
        if key == 27:
            break

def check_uso():
    alerta = 0
    while True:
        data = datetime.now().strftime('%d-%m-%y')
        data_atual = datetime.now().strftime('%d-%m-%y %H:%M')
        time.sleep(5)
        try:
            pc_em_uso = check_face_existente()
            if pc_em_uso[0] == True:
                usuario = pc_em_uso[1]
                print(usuario)
                mongodb.get_dados_acesso(data, usuario, 7)
                idade = int(mongodb.get_idade_usuario(usuario))
                if idade >=11 and idade <= 18:
                    hora = datetime.now().strftime('%H:%M')
                    if hora > '01:00' and hora <= '06:00':
                        alerta +=1
                        if alerta % 60 == 0:
                            mensagem = 'entre 11 e 18 anos:\nEvitar deixar que os adolescentes virem a noite em jogos e outras atividades do tipo.'
                            telegram.envio_de_alerta(f'Usuário {usuario} está a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nData de Alerta: {data_atual}')
                            alerta = 0
        except Exception as err:
            pass

check_uso()