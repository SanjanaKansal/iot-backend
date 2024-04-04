#!/usr/bin/env bash

# Usage
usage() {
    echo "Usage: $0 host:port [-- command args]"
    exit 1
}

# Argument Parsing
HOST=""
PORT=""
COMMAND=()

# Parse the host and port
if [[ "$#" -eq 0 ]]; then
    usage
fi

HOSTPORT=($(echo $1 | tr ':' '\n'))
if [ "${#HOSTPORT[@]}" -ne 2 ]; then
    echo "Error: Invalid host:port argument."
    usage
fi

HOST=${HOSTPORT[0]}
PORT=${HOSTPORT[1]}

# Validate port is a number
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: Port must be an integer."
    usage
fi

shift
if [[ "$#" -gt 0 ]]; then
    COMMAND=("$@")
fi

# Wait for the host:port to be available
echo "Waiting for ${HOST}:${PORT} - checking connectivity..."
while ! timeout 1 bash -c "echo > /dev/tcp/${HOST}/${PORT}" 2>/dev/null; do
    echo "Still waiting for ${HOST}:${PORT}..."
    sleep 1
done

echo "${HOST}:${PORT} is now available!"

# Execute the command if specified
if [ ${#COMMAND[@]} -gt 0 ]; then
    echo "Executing command: ${COMMAND[*]}"
    exec "${COMMAND[@]}"
fi
