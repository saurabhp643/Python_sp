import pika
import json

class EventBus:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish(self, event_name, event_data):
        """Publish an event to RabbitMQ"""
        event = json.dumps({"event": event_name, "data": event_data})
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=event)
        print(f"📢 Published event: {event_name} → {event_data}")

    def subscribe(self, callback):
        """Subscribe to an event"""
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message["data"])

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=wrapper, auto_ack=True)
        print(f"📥 Listening for events on {self.queue_name}...")
        self.channel.start_consuming()
