.PHONY: lint
lint: 
	black **/ --check

.PHONY: test
test:
	pytest .

.PHONY: create-topics
create-topics:
	docker exec -it grabber-backend-kafka-1 /opt/kafka-startup-scripts/create-topics.sh
