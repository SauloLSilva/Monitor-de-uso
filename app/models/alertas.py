from app.models.mongodb import Mongodatabase
from datetime import datetime, timedelta
from app.models.bot_telegram import Bot_alerta
from app.models.email import Email
from app.models.dashboards import Gerar_grafico

mongodb = Mongodatabase()
telegram = Bot_alerta()
email = Email()
mensagens = list()
gerar_grafico = Gerar_grafico()

class alertas(object):
    def monitoramento_hora_dia(self, tipo_alerta):
        registro = 0
        data_atual = datetime.now().strftime('%d-%m-%y %H:%M')

        usuarios = mongodb.get_registro_de_uso(data_atual.split(' ')[0])

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
                mensagem = f'\nUsuário {nome} esteve a frente do PC por {tempo_de_uso} minuto(s)\nIdade: {idade} ano(s)'
                mensagens.append(mensagem)

        if mensagens.count != 0 and tipo_alerta == 'dia':
            mensagem_telegram = ', '.join(mensagens)
            telegram.envio_de_alerta('Seu Relatorio diário do dia {}:\n{}'.format(data_atual.split('.')[0], mensagem_telegram))
            email.sender(mensagem_telegram)

        if registro == 0 and tipo_alerta == 'hora':
            mensagem = f'Sem Utilização do PC no momento\nData: {data_atual}'
            telegram.envio_de_alerta(mensagem)

        if registro == 0 and tipo_alerta == 'dia':
            mensagem = ('Dia {} não teve utilização do PC'.format(data_atual.split(' ')[0]))
            telegram.envio_de_alerta(mensagem)
            email.sender(mensagem)

        if registro != 0 and tipo_alerta == 'dia':
            telegram.envio_imagem('relatorio_diario')

    def monitoramento_semanal(self, nome, idade):
        try:
            registro = 0
            telegram.envio_de_alerta('Seu Relatório Semanal')
            data_atual = datetime.now()
            datas = [data_atual - timedelta(days=i+1) for i in range(6, -1, -1)]
            get_dados_mongo = [data.strftime('%d-%m-%y') for data in datas]
            dias_da_semana = get_dados_mongo

            for dia in get_dados_mongo:
                data = Mongodatabase().get_registro_de_uso_semanal(dia, nome)
                for dados in data:
                    registro +=1
                    tempo_de_uso = (str(dados['tempo_de_uso']).split('.')[0])
                    if idade >=2 and idade < 6:
                        if tempo_de_uso >= 60:
                            mensagem = 'entre 2 e 5 anos:\nLimitar a uma hora por dia, sempre com supervisão de um adulto;'
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nDia: {dia}')
                        else:
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}\nDia: {dia}')

                    elif idade >=6 and idade <= 11:
                        if tempo_de_uso >= 120:
                            mensagem = 'entre 6 e 10 anos:\nLimitar o tempo de tela a uma ou duas horas por dia, sempre com supervisão;'
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nDia: {dia}')
                        else:
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}\nDia: {dia}')

                    elif idade >=11 and idade <= 18:
                        if tempo_de_uso >= 180:
                            mensagem = 'entre 11 e 18 anos:\nManter a exposição às telas entre 2 a 3 horas por dia, com supervisão. Evitar deixar que os adolescentes virem a noite em jogos e outras atividades do tipo.'
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nSegundo Sociedade Brasileira de Pediatria (SBP), {mensagem}\nIdade: {idade} ano(s)\nDia: {dia}')
                        else:
                            telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}\nDia: {dia}')
                    else:
                        telegram.envio_de_alerta(f'Usuário {nome} esteve a {tempo_de_uso} minutos a frente do PC\nIdade: {idade}\nDia: {dia}')

            if registro == 0:
                telegram.envio_de_alerta(f'Usuário {nome} Não Utilizou o PC durante o período de {dias_da_semana[0]} e {dias_da_semana[-1]}')
            else:
                gerar_grafico.grafico_individual(nome, idade)
                telegram.envio_imagem('monitoramento_individual')
        except Exception as err:
            print(err)