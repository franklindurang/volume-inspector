FROM python:3.9-slim-buster
WORKDIR /app
COPY list_files.py .
CMD ["python", "list_files.py", "/data"]
