import socket
import os
from datetime import datetime
from app.models.mongodb import Mongodatabase
import subprocess

try:
    subprocess.check_output(['sudo', 'service', 'mongod', 'start'])
except:
    pass

mongodb = Mongodatabase()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

# print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

def get_logged_in_user():
    #coleta usuário logado
    try:
        cmd = os.popen("who").read()
        usuarios = cmd.strip().split("\n")
        usuario_logado = [usuario.split()[0] for usuario in usuarios]
        return usuario_logado[0]
    except Exception as e:
        pass


def check_uso():
    while True:
        data = datetime.now().strftime('%d-%m-%y')
        try:
            message, address = sock.recvfrom(4096)
            if message != '':
                dados = bool(message.decode('utf-8').split(','))
                if dados == True:
                    usuario = get_logged_in_user()
                    mongodb.get_dados(data, usuario, 5)
        except KeyboardInterrupt:
            print('CTRL-C')
            break
        except Exception as err:
            pass

check_uso()