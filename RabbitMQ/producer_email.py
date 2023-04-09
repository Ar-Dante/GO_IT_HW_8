import pika
import sys
import os

from mongoengine import connect

from model import Contact


def main():
    connect(host="mongodb://localhost:27017/hw8")

    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="email")

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contact.objects.get(id=contact_id)
        print(f"Sending email to {contact.fullname}...")
        contact.message_sent = True
        contact.save()

    channel.basic_consume(queue="email", on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
