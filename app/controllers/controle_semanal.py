#importando o app do projeto principal
from app import app
from flask import render_template, request, redirect, url_for
from app.models.mongodb import Mongodatabase
from app.models.dashboards import Gerar_grafico
from app.models.bot_telegram import Bot_alerta


mongodb = Mongodatabase()
telegram = Bot_alerta()
grafico = Gerar_grafico()

@app.route('/controle_semanal', methods=['GET', 'POST'])
def controle_semanal():

    if request.method == 'POST':
        data = request.form
        id = data.get('usuario_id')
        dados = mongodb.get_id_colaborador(id)
        grafico.grafico_individual(dados[0], dados[1])

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