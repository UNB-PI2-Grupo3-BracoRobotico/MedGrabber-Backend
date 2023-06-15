.PHONY: lint
lint: 
	black **/ --check

.PHONY: test
test:
	pytest .