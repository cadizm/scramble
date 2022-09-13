all: build

build:
	docker build --tag cadizm/scramble .

docker-run: build
	docker run --rm -p 9002:9002 cadizm/scramble

push:
	docker push cadizm/scramble:latest

deploy:
	ansible-playbook --inventory ansible/hosts --limit=dev --user=cadizm ansible/deploy.yml
