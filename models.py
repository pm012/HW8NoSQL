import json
from mongoengine import connect, Document, StringField, ListField, ReferenceField

# Connect to MongoDB
connect("mongodb+srv://sergeykroshkaw:sh96JVrCcrOxfwfi@cluster0.fmy6b5c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Define MongoDB models
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Load JSON data into MongoDB
def load_authors_from_json(filename):
    with open(filename, "r") as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            Author(**author_data).save()

def load_quotes_from_json(filename):
    with open(filename, "r") as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data["author"]
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data["author"] = author
                Quote(**quote_data).save()

# Search quotes by tag or author name
def search_quotes(command):
    if command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return [quote.to_json().encode("utf-8") for quote in quotes]
        else:
            return []

    elif command.startswith("tag:"):
        tags = command.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        return [quote.to_json().encode("utf-8") for quote in quotes]

    elif command == "exit":
        return "Exiting..."

    else:
        return "Invalid command!"

# Load JSON data into MongoDB collections
load_authors_from_json("./json/authors.json")
load_quotes_from_json("./json/quotes.json")

# Search quotes in an endless loop
while True:
    command = input("Enter command (name:, tag:, exit): ")
    result = search_quotes(command)
    if result:
        for item in result:
            print(item.decode("utf-8"))
    else:
        print("No quotes found.")
