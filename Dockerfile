FROM  python:3.11.6-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

WORKDIR .
COPY ./ ./

CMD ["python3","main.py" ]  