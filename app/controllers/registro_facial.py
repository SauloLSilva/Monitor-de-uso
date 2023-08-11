import os
from app import app
from flask import render_template, request, redirect, url_for, flash
import cv2
from app.models.simple_facerec import SimpleFacerec
from werkzeug.utils import secure_filename
import subprocess
from datetime import datetime

validador = SimpleFacerec()

@app.route('/registro_facial', methods=['GET', 'POST'])
def registro_facial():
    if request.method == 'POST':
        nome = request.form['name']
        imagem = request.files['image']

        if imagem and allowed_file(imagem.filename):
            timestamp = str(datetime.now()).split('.')[1]
            filename = secure_filename(imagem.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{nome}_{timestamp}.jpg')
            imagem.save(image_path)
            try:
                retorno = validador.load_encoding_images()
                mensagem = f'Cadastro de {nome} concluído'
                return render_template('registro_facial.html', message=mensagem, image_path=image_path)
            except Exception as err:
                mensagem = f'Erro ao cadastrar {nome}'
                rota = str(subprocess.check_output(['pwd']).decode('utf-8'))[:-1]
                rota = f'{rota}/app/static/img/'
                os.remove(f"{rota}/{nome}_{timestamp}.jpg")
                return render_template('registro_facial.html', message=mensagem, image_path=image_path)

    return render_template('registro_facial.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
