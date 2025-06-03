FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y curl nano

# Create mount directory before the volume mounts
RUN mkdir -p /mnt/data

WORKDIR /mnt/data
CMD ["sleep", "infinity"]
