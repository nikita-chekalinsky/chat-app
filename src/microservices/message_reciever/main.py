import pika
import json
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='send_notification_1')
channel.basic_publish(exchange='',
                      routing_key='send_notification_1',
                      body=json.dumps({"msg": 'Hello World!',
                                       "client_id": "234-4567"}))
connection.close()
print(" [x] Sent 'Hello World!'")
