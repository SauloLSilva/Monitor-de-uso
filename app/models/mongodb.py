from pymongo import MongoClient

class Mongodatabase(object):
    def server(self):
        client = MongoClient("mongodb://localhost:27017")
        db = client['gestao_de_acesso']
        return db
    
    def insert_dados(self, data, usuario, tempo):
        collection = self.server()[data]
        dados = [
            {'nome':usuario, 'tempo_de_uso':tempo/60},
        ]
        collection.insert_many(dados)

    def get_dados(self, data, usuario, tempo):
        collection = self.server()[data]
        query = {'nome': usuario}
        registro_usuario = collection.count_documents(query)
        if registro_usuario:
            update = collection.update_one({'nome': usuario}, {'$inc': {'tempo_de_uso':tempo/60}})
        else:
            self.insert_dados(data, usuario, tempo)

    def get_registro_de_uso(self, data):
        collection = self.server()[data]
        dados = collection.find()
        for dado in dados:
            return dado