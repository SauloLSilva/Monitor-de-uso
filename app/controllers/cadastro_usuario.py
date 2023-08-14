from flask import render_template, request, redirect, url_for, flash
from app import app
from app.models.mongodb import Mongodatabase

mongodb = Mongodatabase().user_data()

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = mongodb.find_one({'username': username})
        if existing_user:
            return render_template('cadastro_usuario.html', message='Usuário Já Cadastrado')

        mongodb.insert_one({'username': username, 'password': password})
        return redirect(url_for('login'))

    return render_template('cadastro_usuario.html')