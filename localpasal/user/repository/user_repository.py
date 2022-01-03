from configs.database import mongodatabase


def add_user(data:dict):
    mongodatabase.user.insert_one(data)
