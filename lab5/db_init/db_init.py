import uuid
import random
from datetime import datetime

import psycopg2
from sqlalchemy.orm import Session
from pymongo import TEXT, mongo_client
from sqlalchemy import URL, create_engine

from models import User, Password


if __name__ == '__main__':
    init_db = False
    with psycopg2.connect(
        database='messanger', user='admin', password='secret', host='postgres', port='5432'
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.users');")
            if cursor.fetchone()[0] is None:
                with open('db_init.sql', 'r', encoding='utf-8') as file:
                    cursor.execute(file.read())
                connection.commit()
                init_db = True
    if init_db:
        print('PostgreSQL is connected')
        engine = create_engine(
            URL.create(
                drivername='postgresql',
                username='admin',
                password='secret',
                host='postgres',
                port='5432',
                database='messanger',
            )
        )
        with Session(engine) as session:
            session.add(
                User(login='admin', name='admin', password=Password.hash_password('secret'))
            )
            for i in range(6):
                session.add(
                    User(
                        login=f'user_{i}',
                        name=f'user_{i}',
                        password=Password.hash_password(f'password_{i}'),
                    )
                )
            session.commit()

    client = mongo_client.MongoClient(host='mongo', port=27017, uuidRepresentation='standard')
    messages = client['messenger']['messages']
    messages.create_index('chat_id')
    messages.create_index([('text', TEXT)])

    for _ in range(5):
        chat_id = uuid.uuid4()
        for index in range(random.randint(1, 5)):
            messages.insert_one(
                {
                    'chat_id': chat_id,
                    'text': f'Text №{index} in {chat_id} chat',
                    'sender_login': 'user',
                    'sending_time': datetime.now(),
                }
            )