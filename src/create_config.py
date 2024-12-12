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

    db = client[os.environ.get("MONGODB_DATABASE", "prd")]

    # CSVファイルの読み込みと初期データの設定
    df = pd.read_csv("entry.csv")

    # 初期値を設定
    documents = []
    for _, row in df.iterrows():
        doc = {
            "name": row["name"],
            "url": row["url"],
            "icon": None,  # アイコンの初期値
            "time": 0  # 最終更新時間の初期値
        }
        documents.append(doc)

    try:
        # entry_urlsコレクションにデータを挿入
        entry_urls = db.entry_urls
        for doc in documents:
            entry_urls.update_one(
                {"name": doc["name"]},
                {
                    "$set": {
                        "url": doc["url"],
                        "icon": doc["icon"]
                    }
                },
                upsert=True
            )

        # last_publishedコレクションに初期データを挿入
        last_published = db.last_published
        for doc in documents:
            last_published.update_one(
                {"name": doc["name"]},
                {"$set": {"time": doc["time"]}},
                upsert=True
            )

        print(f"データ投入完了: {len(documents)}件")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    load_csv_to_mongodb()
