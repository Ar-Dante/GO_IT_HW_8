import json
from mongoengine import disconnect

from models import Authors, Qoutes


def load_from_authors():
    with open("authors.json", encoding="UTF-8") as f:
        data = json.load(f)

    for author in data:
        fullname = author.get("fullname")
        born_date = author.get("born_date")
        born_location = author.get("born_location")
        description = author.get("description")
        new_author = Authors(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )
        new_author.save()


def load_from_quotes():
    with open("qoutes.json", encoding="UTF-8") as f:
        data = json.load(f)

    for one_quote in data:
        tags = one_quote.get("tags")
        quote = one_quote.get("quote")
        authors = Authors.objects(fullname=one_quote.get("author"))
        new_quote = Qoutes(tags=tags, quote=quote, author=authors[0])
        new_quote.save()


if __name__ == "__main__":
    load_from_authors()
    load_from_quotes()
