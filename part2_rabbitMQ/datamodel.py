from mongoengine import Document, StringField, EmailField, BooleanField, IntField

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    sent_email = BooleanField(default=False)
    sent_sms = BooleanField(default=False)
    best_way_to_send = StringField(choises=["email","sms"], default="email")
