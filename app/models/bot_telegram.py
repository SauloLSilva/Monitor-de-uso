import telegram
import subprocess

class Bot_alerta(object):
    def token_api(self):
        # Defina o token de acesso do seu bot aqui
        return '6089265882:AAGwlx8NAq4RC4QbVLPeSb_nouICZJF98Yk', '-914116709'

    def envio_de_alerta(self, mensagem):

        # Crie um objeto bot com o seu token de acesso
        bot = telegram.Bot(self.token_api()[0])

        # Envie uma mensagem para o seu bot
        bot.send_message(self.token_api()[1], text=mensagem)
        
        return True
    
    def envio_imagem(self):
        rota = str(subprocess.check_output(['pwd']).decode('utf-8'))[:-1]
        rota = f'{rota}/app/static/graphs/relatorio_diario.png'

        # Crie um objeto bot com o seu token de acesso
        bot = telegram.Bot(self.token_api()[0])

        # Envie uma mensagem para o seu bot
        bot.send_photo(self.token_api()[1], photo=open(rota, 'rb'))        
        return True
        