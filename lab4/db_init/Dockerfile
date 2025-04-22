FROM python:3.12

ENV TZ=Europe/Moscow
ENV PYTHONPATH=/user_sqldb_init

RUN mkdir /user_db
COPY . /user_db
WORKDIR /user_db

RUN pip install --upgrade pip 
RUN pip install -r  db_init_requirements.txt

CMD [ "python", "db_init.py"]