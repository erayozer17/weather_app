run:
	pip freeze > requirements.txt && cd app && django-admin compilemessages && cd .. && docker-compose up -d --build