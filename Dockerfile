FROM python:3.10-slim

WORKDIR /data

EXPOSE 80

CMD ["python3", "-m", "http.server", "80"]
