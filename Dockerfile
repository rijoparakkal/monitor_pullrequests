FROM python:latest
MAINTAINER Author Rijo Joseph <rijoparakkal@gmail.com>
WORKDIR /app
RUN pip install --no-cache-dir requests
COPY git.py .
CMD [ "python", "git.py" ]