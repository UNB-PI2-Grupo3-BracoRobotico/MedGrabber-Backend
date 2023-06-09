#!/bin/bash
# create-topics.sh

set -e

# loop until Kafka is available, then create topics
until kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test-topic; do
  echo "Kafka server is not yet ready"
  sleep 1
done

echo "test-topic created"
