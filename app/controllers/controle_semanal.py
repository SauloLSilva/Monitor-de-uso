#importando o app do projeto principal
from app import app
from flask import render_template

@app.route('/controle_semanal')
def controle_semanal():
    return render_template('controle_semanal.html')