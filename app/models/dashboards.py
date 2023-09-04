import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
from app.models.mongodb import Mongodatabase
import subprocess

class Gerar_grafico(object):

    def grafico_diario(self):

        try:
            subprocess.check_output(['rm', 'app/static/graphs/relatorio_diario.png'])
        except:
            pass

        data_atual = datetime.now().strftime('%d-%m-%y %H:%M')
        cores = list()
        usuarios = list()
        minutos_de_uso_sessao = list()
        mongodb = Mongodatabase()

        verde = '#008000'
        amarelo = "#FFD700"
        vermelho = "#8B0000"
        paleta_de_cores = [verde, amarelo, vermelho]
        declaracao_cores = ['Bom', 'Elevado','Muito Elevado']
        registro_acesso = mongodb.get_registro_de_uso(data_atual.split(' ')[0])

        for usuario in registro_acesso:
            nome = usuario['nome']
            tempo_de_uso = int(str(usuario['tempo_de_uso']).split('.')[0])
            idade = int(mongodb.get_idade_usuario(nome))
            if idade > 0 and idade <= 18:
                minutos_de_uso_sessao.append(tempo_de_uso)
                usuarios.append(f'{nome}({idade})')

            if idade >=2 and idade < 6:
                if tempo_de_uso >= 60 and tempo_de_uso <= 75:
                    cores.append(amarelo)
                elif tempo_de_uso > 75:
                    cores.append(vermelho)
                else:
                    cores.append(verde)

            elif idade >=6 and idade <= 11:
                if tempo_de_uso >= 120 and tempo_de_uso <= 135:
                    cores.append(amarelo)
                elif tempo_de_uso > 135:
                    cores.append(vermelho)
                else:
                    cores.append(verde)

            elif idade >=11 and idade <= 18:
                if tempo_de_uso >= 180 and tempo_de_uso <= 195:
                    cores.append(amarelo)
                elif tempo_de_uso > 195:
                    cores.append(vermelho)
                else:
                    cores.append(verde)

        try:

            sns.set(style="whitegrid")
            plt.figure(figsize=(8, 6))
            ax = sns.barplot(x=minutos_de_uso_sessao, y=usuarios, palette=cores)

            plt.ylabel("Pessoas(Idade)")
            plt.xlabel("Tempo(Minutos)")
            plt.title(f"Tempo de uso, Idade entre 2 a 18 anos\nData: {data_atual}")

            color_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(paleta_de_cores, declaracao_cores)]

            plt.legend(handles=color_patches, bbox_to_anchor=(1.02, 0.5), loc='center left')

            plt.tight_layout()

            for i, v in enumerate(minutos_de_uso_sessao):
                ax.text(v + 1, i, str(v), ha='left', va='center', fontsize=10)

            
            plt.savefig ('app/static/graphs/relatorio_diario.png')
            plt.close()
        except Exception as err:
            print(err)

    def grafico_individual(self, nome, idade):

        idade = int(idade)
        try:
            subprocess.check_output(['rm', 'app/static/graphs/monitoramento_individual.png'])
        except:
            pass

        verde = '#008000'
        amarelo = "#FFD700"
        vermelho = "#8B0000"
        azul = '#1a1a79'
        paleta_de_cores = [verde, amarelo, vermelho, azul]
        declaracao_cores = ['Bom', 'Elevado','Muito Elevado', '18+']

        data_atual = datetime.now()
        datas = [data_atual - timedelta(days=i+1) for i in range(6, -1, -1)]
        get_dados_mongo = [data.strftime('%d-%m-%y') for data in datas]

        dias_da_semana = get_dados_mongo
        acesso_semanal = list()
        cores = list()


        for dia in dias_da_semana:
            try:
                tempo_de_uso = Mongodatabase().get_registro_de_uso_semanal(dia, nome)
                if '.' in str(tempo_de_uso):
                    tempo_de_uso = int(str(tempo_de_uso).split('.')[0])
                acesso_semanal.append(tempo_de_uso)
                if idade >=2 and idade < 6:
                    if tempo_de_uso >= 60 and tempo_de_uso <= 75:
                        cores.append(amarelo)
                    elif tempo_de_uso > 75:
                        cores.append(vermelho)
                    else:
                        cores.append(verde)

                elif idade >=6 and idade <= 11:
                    if tempo_de_uso >= 120 and tempo_de_uso >= 135:
                        cores.append(amarelo)
                    elif tempo_de_uso > 135:
                        cores.append(vermelho)
                    else:
                        cores.append(verde)
                elif idade >=11 and idade <= 18:
                    if tempo_de_uso >= 180 and tempo_de_uso >= 195:
                        cores.append(amarelo)
                    elif tempo_de_uso > 195:
                        cores.append(vermelho)
                    else:
                        cores.append(verde)
            except:
                cores.append(verde)
                acesso_semanal.append(0)

        try:
            sns.set(style="whitegrid")
            plt.figure(figsize=(8, 6))
            ax = sns.barplot(x=acesso_semanal, y=dias_da_semana, palette=cores)

            plt.ylabel("Data")
            plt.xlabel("Tempo(Minutos)")
            plt.title(f"Tempo de uso do Usuário {nome} ({idade} Ano(s))\n{dias_da_semana[0]} - {dias_da_semana[-1]}")

            color_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(paleta_de_cores, declaracao_cores)]

            plt.legend(handles=color_patches, bbox_to_anchor=(1.02, 0.5), loc='center left')

            plt.tight_layout()

            for i, v in enumerate(acesso_semanal):
                ax.text(v + 1, i, str(v), ha='left', va='center', fontsize=10)


            plt.savefig ('app/static/graphs/monitoramento_individual.png')
            plt.close()
        except Exception as err:
            print(err)
