from pymongo import MongoClient
from interface.util.mongodb import MongoDB  # インターフェースクラスは別途定義が必要


class MongoDBImpl(MongoDB):
    def __init__(self, connection_string: str):
        """
        MongoDB Atlasへの接続を初期化します

        Args:
            connection_string: MongoDB接続文字列
            例: "mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority"
        """
        self.client = MongoClient(connection_string)

    def get_instance(self):
        """
        MongoClientインスタンスを返します
        """
        return self.client
