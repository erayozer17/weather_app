run:
	cd app && django-admin compilemessages && cd .. && docker-compose up -d --build

stop:
	docker-compose down -v

test:
	docker-compose run --rm api flake8 && docker-compose run --rm api python manage.py test