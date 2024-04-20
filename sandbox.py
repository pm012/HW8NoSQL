
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
mongo_user = config.get('DB', 'user')
mongo_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


uri = f"""mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"""

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)