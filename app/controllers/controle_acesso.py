#importando o app do projeto principal
from app import app
from flask import render_template, request, redirect, url_for
from app.models.mongodb import Mongodatabase
from datetime import datetime
from app.models.alertas import alertas

mongodb = Mongodatabase()
alerta = alertas()

def get_first_digit(number):
    return int(str(number).split('.')[0])

@app.route('/controle_acesso', methods=['GET', 'POST'])
def controle_acesso():
    if request.method == 'POST':
        alerta.monitoramento_hora_dia('dia')
        return redirect(url_for('pagina_inicial'))
    try:
        data_atual = datetime.now().strftime('%d-%m-%y')
        usuarios = [mongodb.get_registro_de_uso(data_atual)]
        for usuario in usuarios:
            data = [{"nome": item["nome"], "tempo_de_uso": get_first_digit(item["tempo_de_uso"])} for item in usuario]
    except Exception as err:
        data = [{"nome":''}, {"tempo_de_uso": ''}]

    return render_template('controle_acesso.html', data=data)