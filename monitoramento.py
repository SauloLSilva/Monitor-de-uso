import schedule
import time
from app.models.alertas import alertas

alerta = alertas()

def get_first_digit(number):
    return int(str(number).split('.')[0])

schedule.every(30).minutes.do(alerta.monitoramento_hora_dia, 'hora')
schedule.every().day.at('23:55').do(alerta.monitoramento_hora_dia, 'dia')

while True:
    schedule.run_pending()
    time.sleep(1)