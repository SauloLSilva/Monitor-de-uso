#init(módulo principal)
from flask import Flask

app = Flask(__name__, static_url_path='/static')

from app.controllers import index, dashboards, pagina_inicial, controle_acesso, cadastro_usuario


# '''instância, recebe variavel name, que recebe um valor 
# para identificar o arquivo a ser executado'''


