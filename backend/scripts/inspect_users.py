from app.config.db import users_collection
from bson.json_util import dumps

def main():
    users = list(users_collection.find({}))
    print(dumps(users, indent=2))

if __name__ == '__main__':
    main()
