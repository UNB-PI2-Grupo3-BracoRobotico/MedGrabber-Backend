from datetime import datetime
import logging
import json

from confluent_kafka import Consumer, Producer, KafkaError

from grabber_backend.config.kafka import (
    KAFKA_BOOTSTRAP_SERVERS,
    AUTO_OFFSET_RESET,
    ORDER_MANAGER_CONSUMER_GROUP_ID,
)

logging.basicConfig(level=logging.INFO)


class KafkaClient:
    AGENT_NAME = "order_service"

    def __init__(self, bootstrap_servers):
        logging.info(f"Initializing {self.AGENT_NAME}...")

        self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": ORDER_MANAGER_CONSUMER_GROUP_ID,
                "auto.offset.reset": AUTO_OFFSET_RESET,
            }
        )

    def delivery_report(self, err, msg):
        if err is not None:
            logging.error("Message delivery failed: {}".format(err))
        else:
            logging.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )

    def produce(self, topic_messages):
        for topic, message in topic_messages.items():
            produced_message = {
                "timestamp": datetime.now().timestamp(),
                "sender": self.AGENT_NAME,
                "message": message,
            }
            self.producer.produce(
                topic,
                self.encode_message(produced_message),
                callback=self.delivery_report,
            )
        self.producer.flush()

    def consume(self, topics):
        self.consumer.subscribe(topics)

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                logging.info(f"Waiting for message")
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            msg_value = json.loads(msg.value().decode("utf-8"))

            if msg_value.get("sender") == self.AGENT_NAME:
                continue

            logging.info(
                'Received message from topic "{}": {}'.format(
                    msg.topic(), msg.value().decode("utf-8")
                )
            )

            self.proccess(msg.topic(), msg_value)

    def close(self):
        self.consumer.close()

    def encode_message(self, message):
        return json.dumps(message).encode("utf-8")

    def proccess(self, topic, message):
        messages_to_send = {
            "order-status": {"order_id": 1, "customer_id": 1, "status": "delivered"}
        }
        kafka_client.produce(messages_to_send)


if __name__ == "__main__":
    kafka_client = KafkaClient(KAFKA_BOOTSTRAP_SERVERS)

    topics = ["order-creation", "order-status"]
    kafka_client.consume(topics)

    kafka_client.close()