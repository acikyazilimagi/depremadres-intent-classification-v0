test-docker:
	docker build -t deprem-intent-classification .
	docker run --rm -it deprem-intent-classification sh -c "pytest"
