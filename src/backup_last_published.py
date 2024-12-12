import os
import json
from pymongo import MongoClient
import certifi

# MongoDB接続設定
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
DATABASE = os.getenv("MONGODB_DATABASE", "prd")
FILEPATH = "backup_last_published.json"

# MongoDBクライアントの初期化
client = MongoClient(
    MONGODB_CONNECTION_STRING,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
    retryWrites=True
)

try:
    # データベースとコレクションの取得
    db = client[DATABASE]
    collection = db.last_published

    # すべてのドキュメントを取得
    last_published = list(collection.find({}, {'_id': 0}))

    # JSONファイルに保存
    with open(FILEPATH, "w") as f:
        json.dump(last_published, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(f"バックアップ中にエラーが発生しました: {str(e)}")
finally:
    client.close()
