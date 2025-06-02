FROM python:3.10-slim

WORKDIR /data

EXPOSE 8080

CMD ["python3", "-m", "http.server", "8080"]
