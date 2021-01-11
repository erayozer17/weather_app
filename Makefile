run:
	cd app && django-admin compilemessages && cd .. && docker-compose up -d --build

stop:
	docker-compose down -v