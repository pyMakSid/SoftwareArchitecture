import psycopg2
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

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