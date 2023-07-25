#importando o app do projeto principal
from app import app
from flask import render_template

@app.route('/pagina_inicial')
def pagina_inicial():
    return render_template('pagina_inicial.html')