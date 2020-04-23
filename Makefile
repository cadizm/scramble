all:
	docker build --tag cadizm/scramble .

run:
	docker run --rm -e PYTHONPATH=/app -p 5001:5001 cadizm/scramble

push:
	docker push cadizm/scramble

.PHONY: all run push
