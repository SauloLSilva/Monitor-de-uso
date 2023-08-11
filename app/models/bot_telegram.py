import telegram

class Bot_alerta(object):
    def envio_de_alerta(self, mensagem):

        # Defina o token de acesso do seu bot aqui
        token = '6089265882:AAGwlx8NAq4RC4QbVLPeSb_nouICZJF98Yk'

        # Crie um objeto bot com o seu token de acesso
        bot = telegram.Bot(token)

        # Envie uma mensagem para o seu bot
        bot.send_message(chat_id='-914116709', text=mensagem)
        
        return True