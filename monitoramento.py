import schedule
import time
from app.models.mongodb import Mongodatabase
from datetime import datetime
from app.models.bot_telegram import Bot_alerta


mongodb = Mongodatabase()
telegram = Bot_alerta()

def get_first_digit(number):
    return int(str(number).split('.')[0])

def check_uso():
    data_atual = datetime.now().strftime('%d-%m-%y')
    usuarios = mongodb.get_registro_de_uso(data_atual)
    for usuario in usuarios:
        tempo = str(usuario['tempo_de_uso']).split('.')[0]
        nome = usuario['nome']
        if int(tempo) >= 55 and int(tempo) <= 65:
            telegram.envio_de_alerta(f'''Usuário {nome} está a {tempo} minutos a frente do PC hoje''')
check_uso()