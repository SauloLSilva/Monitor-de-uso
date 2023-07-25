#importando o app do projeto principal
from app import app
from flask import render_template

'''usado para definir rota função abaixo, não esquecer
de usar a rule (caminho entre parentesis)'''
@app.route('/')
def index():
    return render_template('login.html')