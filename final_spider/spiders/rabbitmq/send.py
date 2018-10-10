import pika

username = 'dio'
pwd = 'dio'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.129', credentials=user_pwd))
chan = s_conn.channel()
chan.queue_declare(queue='sporttery_tickets', durable=True)

for t in range(1, 1000):
    msg = str(t) + '-' + str(t + 1) + '-' + str(t + 2) + ',' + str(t + 3) + '-' + str(t + 4)
    chan.basic_publish(exchange='', routing_key='sporttery_tickets', body=msg, properties=pika.BasicProperties(delivery_mode=2))
    print("[生产者] " + msg)

chan.close()
s_conn.close()
