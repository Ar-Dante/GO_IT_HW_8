import pika
from faker import Faker
from mongoengine import connect
from model import Contact
import random

fake = Faker()
SEND_METHOD = ["SMS", "E-mail"]

connect(host="mongodb://localhost:27017/hw8")

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="email")
channel.queue_declare(queue="sms")


def main():
    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        send = fake.boolean()
        send_method = random.choice(SEND_METHOD)
        contact = Contact(
            fullname=fullname,
            email=email,
            phone=phone,
            send=send,
            send_method=send_method,
        )
        contact.save()

        body = str(contact.id)
        match send_method:
            case "SMS":
                channel.basic_publish(exchange="", routing_key="sms", body=body)
            case "E-mail":
                channel.basic_publish(exchange="", routing_key="email", body=body)
    connection.close()


if __name__ == "__main__":
    main()
