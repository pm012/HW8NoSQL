import configparser
import pika

config = configparser.ConfigParser()
config.read('config.ini')
rm_user = config.get('RABBIT_MQ', 'user')
rm_pass = config.get('RABBIT_MQ', 'password')
rm_host = config.get('RABBIT_MQ', 'host')
rm_port = config.get('RABBIT_MQ', 'port')

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(rm_user, rm_pass)
    return pika.BlockingConnection(pika.ConnectionParameters(host=rm_host, port=rm_port, credentials=credentials))