import os
from app import app
from flask import render_template, request
import cv2
from app.models.simple_facerec import SimpleFacerec
from werkzeug.utils import secure_filename
import subprocess
from datetime import datetime
from app.models.mongodb import Mongodatabase
import signal

validador = SimpleFacerec()
mongodb = Mongodatabase()

def reiniciar_monitoramento():
    try:
        # Encerra o processo atual
        processo_atual = subprocess.Popen(["pgrep", "-f", "identificador.py"], stdout=subprocess.PIPE)
        processos_ids = processo_atual.stdout.read().decode().split()
        for pid in processos_ids:
            os.kill(int(pid), signal.SIGTERM)

        # Inicia o script novamente
        subprocess.Popen(["python3", "identificador.py"])

    except:
        pass

@app.route('/registro_facial', methods=['GET', 'POST'])
def registro_facial():
    if request.method == 'POST':
        nome = request.form['name']
        imagem = request.files['image']
        idade = request.form['age']

        if imagem and allowed_file(imagem.filename):
            timestamp = str(datetime.now()).split('.')[1]
            filename = secure_filename(imagem.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{nome}_{timestamp}.jpg')
            cadastro_existente = mongodb.validacao_cadastro(nome)
            if cadastro_existente == True:
                mensagem = f'{nome} Já Cadastrado'
                return render_template('registro_facial.html', message=mensagem, image_path=image_path)
            else:
                imagem.save(image_path)
                try:
                    retorno = validador.load_encoding_images()
                    cadastro = mongodb.cadastro_usuario(nome, idade)
                    mensagem = f'Cadastro de {nome} concluído'
                    reiniciar_monitoramento()
                    return render_template('registro_facial.html', message=mensagem, image_path=image_path)

                except Exception as err:
                    mensagem = f'Erro ao cadastrar foto de {nome}, não foi possível identificar rosto em imagem enviada.'
                    rota = str(subprocess.check_output(['pwd']).decode('utf-8'))[:-1]
                    rota = f'{rota}/app/static/img/'
                    os.remove(f"{rota}/{nome}_{timestamp}.jpg")
                    return render_template('registro_facial.html', message=mensagem)

    return render_template('registro_facial.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS