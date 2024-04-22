import sys
sys.path.append('.')
from rabbitmq_connection import get_rabbitmq_connection
from connect import get_mongo_connection
from datamodel import Contact

mediatypes = {
    "email": "email_queue",
    "sms": "sms_queue"
}

def handle_contact_message(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if not contact.sent_email and contact.best_way_to_send == "email":
            # Stub function for sending email implementation 
            print(f"Sending email to {contact.email}")
            contact.sent_email = True
            contact.save()

        elif not  contact.sent_sms and contact.best_way_to_send == "sms":
            # Stub function for sending SMS
            print(f"Sending SMS to {contact.phone_number}")
            contact.sent_sms = True
            contact.save()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with get_mongo_connection():
        with get_rabbitmq_connection() as connection:        
            channel = connection.channel()
            channel.queue_declare(queue=mediatypes["email"])
            channel.queue_declare(queue=mediatypes["sms"])
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=mediatypes["email"], on_message_callback=handle_contact_message)
            channel.basic_consume(queue=mediatypes["sms"], on_message_callback=handle_contact_message)

            print("Waiting for messages. To exit press CTRL_C")
            channel.start_consuming()


if __name__ == "__main__":
    main()



    