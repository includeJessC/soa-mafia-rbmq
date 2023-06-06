FROM python

WORKDIR /app
COPY ../.. .
COPY rbmq .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "rbmq.py" ]