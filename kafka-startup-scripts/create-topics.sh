#!/bin/bash
# create-topics.sh

KAFKA_BROKER=kafka:9092
ZOOKEEPER=zookeeper:2181

# define topics
topics=("order-creation" "order-status" "payment" "order-products")

# Create topics
for TOPIC in "${topics[@]}"; do
    echo "Creating topic: $TOPIC"
    kafka-topics.sh --create --if-not-exists --zookeeper $ZOOKEEPER --partitions 1 --replication-factor 1 --topic $TOPIC
done

echo "Topic creation completed."