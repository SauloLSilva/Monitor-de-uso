from pymongo import MongoClient

class Mongodatabase(object):
    def server(self):
        client = MongoClient("mongodb://localhost:27017")
        db = client['gestao_de_acesso']
        return db
    
    def user_data(self):
        db = self.server()
        collection = db['users']
        return collection
    
    def validacao_cadastro(self, usuario):
        collection = self.server()['cadastros']
        query = {'nome': usuario}
        registro_usuario = collection.count_documents(query)
        if registro_usuario:
            return True
        else:
            return False
        
    def cadastro_usuario(self, usuario, idade):
        collection = self.server()['cadastros']
        dados = [
            {'nome':usuario, 'idade':idade},
        ]
        collection.insert_many(dados)


    def insert_dados_acesso(self, data, usuario, tempo):
        collection = self.server()[data]
        query = {'nome': usuario}
        registro_usuario = collection.count_documents(query)
        if registro_usuario:
            update = collection.update_one({'nome': usuario}, {'$inc': {'tempo_de_uso':tempo/60}})
        else:
            dados = [
                {'nome':usuario, 'tempo_de_uso':tempo/60},
            ]
            collection.insert_many(dados)

    def get_dados_acesso(self, data, usuario, tempo):
        collection = self.server()['cadastros']
        query = {'nome': usuario}
        registro_usuario = collection.count_documents(query)
        if registro_usuario:
            self.insert_dados_acesso(data, usuario, tempo)

    def get_registro_de_uso(self, data):
        collection = self.server()[data]
        dados = collection.find()
        return dados
    
    def get_idade_usuario(self, usuario):
        collection = self.server()['cadastros']
        dados = collection.find({'nome':usuario})
        for usuario in dados:
            return usuario['idade']
        
    def get_email_cadastrado(self):
        collection = self.server()['users']
        dados = collection.find()
        lista = list()
        for usuario in dados:
            email =  usuario['username']
            if email not in lista:
                lista.append(email)
        return lista