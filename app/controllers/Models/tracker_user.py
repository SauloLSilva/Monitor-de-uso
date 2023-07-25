import psutil
import datetime
import os

class Tracker(object):
    def get_system_uptime(self):
        #coleta dados de uso do pc
        coletar_dados = psutil.boot_time()
        hora_atual = datetime.datetime.now().timestamp()
        tempo__ativo = hora_atual - coletar_dados
        return tempo__ativo

    def format_uptime(self, tempo__ativo):
        #formata data em padrao de horas
        tempo__ativo = int(tempo__ativo)
        horas, segundos_restantes = divmod(tempo__ativo, 3600)
        minutos, segundos = divmod(segundos_restantes, 60)
        return f"{horas} Hora(s), {minutos} Minuto(s), e {segundos} Segundo(s)"

    def get_logged_in_user(self):
        #coleta usuário logado
        try:
            who_output = os.popen("who").read()
            lines = who_output.strip().split("\n")
            logged_in_users = [line.split()[0] for line in lines]
            return logged_in_users
        except Exception as e:
            pass

    def dados_de_uso(self):
        uptime_seconds = self.get_system_uptime()
        formatted_uptime = self.format_uptime(uptime_seconds)
        logged_in_users = self.get_logged_in_user()
        return [f"Utilização: {formatted_uptime}", f"Usuário: {logged_in_users[0]}"]
