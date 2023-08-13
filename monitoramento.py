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
        nome = usuario['nome']
        tempo_de_uso = int(str(usuario['tempo_de_uso']).split('.')[0])
        idade = mongodb.get_idade_usuario(nome)
        nome = usuario['nome']
        if tempo_de_uso >= 25 and tempo_de_uso <= 30:
            telegram.envio_de_alerta(f'''Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}Ano(s)\nData: {data_atual}''')

check_uso()