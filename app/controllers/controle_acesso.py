#importando o app do projeto principal
from app import app
from flask import render_template

@app.route('/controle_acesso')
def controle_acesso():
    return render_template('controle_acesso.html')