#importando o app do projeto principal
from app import app
from flask import render_template, request, redirect, url_for
from app.models.mongodb import Mongodatabase
from app.models.dashboards import Gerar_grafico
from app.models.bot_telegram import Bot_alerta
from app.models.alertas import alertas


mongodb = Mongodatabase()
telegram = Bot_alerta()
grafico = Gerar_grafico()
alerta = alertas()

@app.route('/controle_semanal', methods=['GET', 'POST'])
def controle_semanal():

    if request.method == 'POST':
        data = request.form
        id = data.get('usuario_id')
        dados = mongodb.get_id_colaborador(id)
        nome = dados[0]
        idade = dados[1]
        alerta.monitoramento_semanal(nome, idade)

    try:
        usuarios = mongodb.get_cadastros()
        usuarios_data = []
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario['_id'],
                'nome': usuario['nome'],
                'idade': usuario['idade']
            })
    except Exception as err:
        usuarios_data = ''

    return render_template('controle_semanal.html', data=usuarios_data)