FROM python:latest

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY git.py .

CMD [ "python", "git.py" ]
