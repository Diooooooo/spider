import time

import pika

username = 'dio'
pwd = 'dio'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.129', credentials=user_pwd))
chan = s_conn.channel()

chan.queue_declare(queue='sporttery_tickets', durable=True)


def callback(ch, method, properties, body):
    print("[消费者1] recv %s, %s" % (body, properties))
    time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)


chan.basic_qos(prefetch_count=1)
chan.basic_consume(callback, queue='sporttery_tickets')
chan.start_consuming()
