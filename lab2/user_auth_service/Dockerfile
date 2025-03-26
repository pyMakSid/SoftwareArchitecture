FROM python:3.12

ENV TZ=Europe/Moscow
ENV PYTHONPATH=/user_service_dir

RUN mkdir /user_service_dir
COPY . /user_service_dir
WORKDIR /user_service_dir

RUN pip install -r requ_user_service.txt

CMD [ "python", "user_service.py" ]