
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]

# Expose the port on which the app will run
EXPOSE 8000

