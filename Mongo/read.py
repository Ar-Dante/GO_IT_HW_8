from functools import wraps

from Mongo.models import Authors, Qoutes
import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def cache(func):
    @wraps(func)
    def wrapper(*args):
        key = func.__name__ + str(args)
        result = r.get(key)
        if result is None:
            result = func(*args)
            r.set(key, str(result))
        return result

    return wrapper


@cache
def get_name(value):
    uuid = Authors.objects(fullname__startswith=value.strip().title())[0]
    quotes = Qoutes.objects(author=uuid)
    for quot in quotes:
        print(quot.quote)


@cache
def get_tag(value):
    quotes = Qoutes.objects(tags__startswith=value)
    for quot in quotes:
        print(quot.quote)


@cache
def get_tags(value):
    quotes = Qoutes.objects(tags__in=value.strip().split(","))
    for quot in quotes:
        print(quot.quote)


def main():
    while True:
        user_command = input("Enter command: ")
        valid_data = user_command.strip().lower()
        if user_command == "exit":
            break
        else:
            try:
                command, value = valid_data.split(":")
                match command:
                    case "name":
                        get_name(value)
                    case "tag":
                        get_tag(value)
                    case "tags":
                        get_tags(value)
                    case _:
                        print("Command is wrong!")
            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
