FROM debian:bullseye-slim

# Make sure /data exists before Railway mounts the volume
RUN mkdir -p /data && apt-get update && apt-get install -y curl nano

# Keep container running so you can inspect it via shell
CMD ["sleep", "infinity"]
