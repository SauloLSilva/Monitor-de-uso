#init(módulo principal)
from flask import Flask
import os

app = Flask(__name__, static_url_path='/static')
try:
    os.mkdir('app/static/img')
    os.mkdir('app/static/graphs')
except:
    pass
app.config['UPLOAD_FOLDER'] = 'app/static/img'

from app.controllers import index, dashboards, pagina_inicial, controle_acesso, cadastro_usuario, registro_facial


# '''instância, recebe variavel name, que recebe um valor 
# para identificar o arquivo a ser executado'''


