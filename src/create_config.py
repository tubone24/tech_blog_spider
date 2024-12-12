import os
from pymongo import MongoClient
import pandas as pd
import certifi

MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
DATABASE = os.getenv("MONGODB_DATABASE", "prd")
FILEPATH = "entry.csv"

def load_csv_to_mongodb():
    # MongoDBクライアントの初期化
    client = MongoClient(
        MONGODB_CONNECTION_STRING,
        tls=True,
        retryWrites=True,
        serverSelectionTimeoutMS=30000
    )

    # データベースとコレクションの取得
    db = client[DATABASE]
    collection = db.entry_urls

    # CSVファイルの読み込み
    df = pd.read_csv(FILEPATH)

    # データをMongoDBのドキュメント形式に変換
    documents = df.to_dict('records')

    # upsert処理の実行
    for doc in documents:
        collection.update_one(
            {"name": doc["name"]},
            {"$set": doc},
            upsert=True
        )

    client.close()

if __name__ == "__main__":
    load_csv_to_mongodb()
