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

def monitoramento_hora_dia(tipo_alerta):
    registro = 0
    data_atual = datetime.now().strftime('%d-%m-%y %H:%M')

    usuarios = mongodb.get_registro_de_uso(data_atual.split(' ')[0])

    if tipo_alerta == 'dia':
        telegram.envio_de_alerta('Seu Relatorio diário do dia {}'.format(data_atual.split(' ')[0]))
    for usuario in usuarios:
        registro += 1
        nome = usuario['nome']
        tempo_de_uso = int(str(usuario['tempo_de_uso']).split('.')[0])
        idade = int(mongodb.get_idade_usuario(nome))
        nome = usuario['nome']
        if tipo_alerta == 'hora':
            if idade >=2 and idade < 6:
                if tempo_de_uso >= 60:
                    mensagem = 'entre 2 e 5 anos:\nLimitar a uma hora por dia, sempre com supervisão de um adulto;'
                    telegram.envio_de_alerta(f'Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nData de Alerta: {data_atual}')

            elif idade >=6 and idade <= 11:
                if tempo_de_uso >= 60:
                    mensagem = 'entre 6 e 10 anos:\nLimitar o tempo de tela a uma ou duas horas por dia, sempre com supervisão;'
                    telegram.envio_de_alerta(f'Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nData de Alerta: {data_atual}')

            elif idade >=11 and idade <= 18:
                if tempo_de_uso >= 120:
                    mensagem = 'entre 11 e 18 anos:\nManter a exposição às telas entre 2 a 3 horas por dia, com supervisão. Evitar deixar que os adolescentes virem a noite em jogos e outras atividades do tipo.'
                    telegram.envio_de_alerta(f'Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nData de Alerta: {data_atual}')

            elif idade > 18:
                telegram.envio_de_alerta(f'Usuário {nome} está a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}\nData: {data_atual}')

        else:
            mensagem = f'Usuário {nome} esteve a frente do PC por {tempo_de_uso} minuto(s)\nIdade: {idade} ano(s)'
            telegram.envio_de_alerta(mensagem)
            email.sender(mensagem)

    if registro == 0 and tipo_alerta == 'hora':
        mensagem = f'Sem Utilização do PC no momento\nData: {data_atual}'
        telegram.envio_de_alerta(mensagem)

    if registro == 0 and tipo_alerta == 'dia':
        mensagem = ('Dia {} não teve utilização do PC'.format(data_atual.split(' ')[0]))
        telegram.envio_de_alerta(mensagem)
        email.sender(mensagem)

schedule.every(30).minutes.do(monitoramento_hora_dia, 'hora')
schedule.every().day.at('23:55').do(monitoramento_hora_dia, 'dia')

while True:
    schedule.run_pending()
    time.sleep(1)