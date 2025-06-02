FROM debian:bullseye-slim

# Create the mount path explicitly
RUN mkdir -p /data && apt-get update && apt-get install -y curl nano

# Keep container alive
CMD ["sleep", "infinity"]
