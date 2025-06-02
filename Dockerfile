FROM debian:bullseye-slim

WORKDIR /data
RUN apt-get update && apt-get install -y curl nano
CMD ["sleep", "infinity"]
