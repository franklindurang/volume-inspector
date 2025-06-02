FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y curl nano && mkdir -p /mnt/data
CMD ["sleep", "infinity"]
