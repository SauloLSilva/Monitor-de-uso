from app import app
from flask import render_template, request, redirect, url_for
from app.models.mongodb import Mongodatabase

mongodb = Mongodatabase().user_data()

'''usado para definir rota função abaixo, não esquecer
de usar a rule (caminho entre parentesis)'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongodb.find_one({'username': username, 'password': password})
        if user:
            return redirect(url_for('pagina_inicial'))
        else:
            return render_template('login.html', message='Erro de Login ou Senha')

    return render_template('login.html')