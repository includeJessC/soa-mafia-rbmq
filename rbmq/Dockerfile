FROM python:3.8

WORKDIR /app
COPY ../.. .
COPY rbmq .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "rbmq.py" ]