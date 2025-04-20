FROM python:3.12

ENV TZ=Europe/Moscow
ENV PYTHONPATH=/messanger_service_dir

RUN mkdir /messanger_service_dir
COPY . /messanger_service_dir
WORKDIR /messanger_service_dir

RUN pip install -r requ_message_service.txt

CMD [ "python", "message_service.py" ]