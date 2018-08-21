import pika


class RabbitMq(object):

    def __init__(self):
        self.username = 'dio'
        self.passwd = 'dio'
        self.host = '192.168.1.129'
        self.exchange_name = ''
        self.routing_key = 'sporttery_tickets'
        user_pwd = pika.PlainCredentials(self.username, self.passwd)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=user_pwd))

    def channel(self):
        return self.conn.channel()

