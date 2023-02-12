build-lint-test:
	docker build -t deprem-intent-classification .
	docker run --rm -it deprem-intent-classification sh -c "flake8 && pytest"
