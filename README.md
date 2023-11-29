extrct the zip file
step 1 install docker on your machine
step 2 cd django-email-master
step 3 cd mail
step 4 docker compose up --build



docker compose will install dependencies. "Rabbitmq, Celery,requirements etc."


for sending emails:
you need to update setting.py

DEFAULT_FROM_EMAIL= ""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_PASSWORD=""
EMAIL_HOST_USER = "apikey"
EMAIL_PORT = "587"
# EMAIL_USE_TLS = "True"
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


update mentioned details in setting.py  


celery:
celery -A mail worker -l info