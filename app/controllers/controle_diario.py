#importando o app do projeto principal
from app import app
from flask import render_template, request, redirect, url_for
from app.models.mongodb import Mongodatabase
from datetime import datetime
from app.models.alertas import alertas
from app.models.dashboards import Gerar_grafico

dados = Gerar_grafico()
mongodb = Mongodatabase()
alerta = alertas()

def get_first_digit(number):
    return int(str(number).split('.')[0])

@app.route('/controle_diario', methods=['GET', 'POST'])
def controle_acesso():
    if request.method == 'POST':
        alerta.monitoramento_hora_dia('dia')
        return redirect(url_for('pagina_inicial'))
    
    try:
        data_atual = datetime.now().strftime('%d-%m-%y')
        usuarios = mongodb.get_registro_de_uso(data_atual)
        
        usuarios_data = []
        for usuario in usuarios:
            idade = mongodb.get_idade_usuario(usuario['nome'])
            if int(idade) > 18:
                usuarios_data.append({
                    'nome': usuario['nome'],
                    'tempo_de_uso': str(usuario['tempo_de_uso']).split('.')[0],
                    'idade': idade
                })
    except Exception as err:
        usuarios_data = ''
    
    dados.grafico_diario()
    
    return render_template('controle_diario.html', data=usuarios_data)