import os
import json
import harperdb

HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")
FILEPATH = "backup_last_published.json"

db = harperdb.HarperDB(
    url=HARPERDB_URL,
    username=HARPERDB_USERNAME,
    password=HARPERDB_PASSWORD,)

last_published = db.sql(f"select * from {HARPERDB_SCHEMA}.last_published")

with open(FILEPATH, "w") as f:
    f.write(json.dumps(last_published))
