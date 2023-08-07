#importando o app do projeto principal
from app import app
from flask import render_template
from app.models.mongodb import Mongodatabase
from datetime import datetime

mongodb = Mongodatabase()
def get_first_digit(number):
    return int(str(number)[0])

@app.route('/controle_acesso')
def controle_acesso():
    data_atual = datetime.now().strftime('%d-%m-%y')
    usuarios = [mongodb.get_registro_de_uso(data_atual)]
    data = [{"nome": item["nome"], "tempo_de_uso": get_first_digit(item["tempo_de_uso"])} for item in usuarios]
    return render_template('controle_acesso.html', data=data)