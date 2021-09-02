import os
import secrets
secret = secrets.token_hex(16)
# MONGO DB SETTINGS
mongo_host = os.environ["MONGODB_HOST"]
mongodb_port = os.environ["MONGODB_PORT"]
mongo_db = os.environ["MONGODB_DB"]
mongo_connect = os.environ["MONGODB_CONNECT"]
mongo_username = os.environ["MONGODB_USERNAME"]
mongo_password = os.environ["MONGODB_PASSWORD"]
mongo_connect = True if mongo_connect == 'True' else False
