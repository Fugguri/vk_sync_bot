FROM  python:3.11.6-bullseye


COPY . .
WORKDIR .
EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["python3","main.py" ]  