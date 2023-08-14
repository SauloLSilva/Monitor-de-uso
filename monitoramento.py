import schedule
import time
from app.models.mongodb import Mongodatabase
from datetime import datetime
from app.models.bot_telegram import Bot_alerta
from app.models.email import Email

mongodb = Mongodatabase()
telegram = Bot_alerta()
email = Email()

def get_first_digit(number):
    return int(str(number).split('.')[0])

def check_uso(tipo_alerta):
    registro = 0
    data_atual = datetime.now().strftime('%d-%m-%y %H:%M')

    usuarios = mongodb.get_registro_de_uso(data_atual.split(' ')[0])

    if tipo_alerta == 'dia':
        pass
        # telegram.envio_de_alerta('Seu Relatorio do dia {}'.format(data_atual.split(' ')[0]))
    for usuario in usuarios:
        registro += 1
        nome = usuario['nome']
        tempo_de_uso = int(str(usuario['tempo_de_uso']).split('.')[0])
        idade = mongodb.get_idade_usuario(nome)
        nome = usuario['nome']
        if tipo_alerta == 'hora':
            if tempo_de_uso >= 110 and tempo_de_uso <= 130:
                telegram.envio_de_alerta(f'Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nIdade: {idade} ano(s)\nData: {data_atual}')
        else:
            mensagem = f'Usuário {nome} esteve a frente do PC {tempo_de_uso} minuto(s)\nIdade: {idade} ano(s)'
            # telegram.envio_de_alerta(mensagem)
            email.sender(mensagem)

    if registro == 0 and tipo_alerta == 'hora':
        mensagem = f'Sem Utilização do PC no momento\nData: {data_atual}'
        telegram.envio_de_alerta(mensagem)

    if registro == 0 and tipo_alerta == 'dia':
        mensagem = ('Dia {} não teve utilização do PC'.format(data_atual.split(' ')[0]))
        telegram.envio_de_alerta(mensagem)
        email.sender(mensagem)

schedule.every(30).minutes.do(check_uso, 'hora')
schedule.every().day.at('23:55').do(check_uso, 'dia')

while True:
    schedule.run_pending()
    time.sleep(1)