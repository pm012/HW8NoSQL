import sys
sys.path.append('.')
from faker import Faker
from connect import get_mongo_connection
from datamodel import Contact
from rabbitmq_connection import get_rabbitmq_connection


mediatypes = {
    "email": "email_queue",
    "sms": "sms_queue"
}


def send_contact_message(contact_id, channel, queue_name):
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=str(contact_id)
    )


def main():
    faker = Faker()
    with get_mongo_connection():
        with get_rabbitmq_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue='email_queue')
            channel.queue_declare(queue='sms_queue')

            for _ in range(100):
                full_name = faker.name()
                email = faker.email()
                phone_number = faker.phone_number()
                best_way_to_send = faker.random_element(elements=list(mediatypes.keys()))
                contact = Contact(
                    full_name=full_name,
                    email = email,
                    phone_number = phone_number,
                    best_way_to_send = best_way_to_send
                )
                contact.save()
            
                send_contact_message(contact.id, channel, mediatypes[best_way_to_send])

if __name__ == "__main__":
    main()

