from app import app
from flask import render_template

@app.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('cadastro_usuario.html')