FROM tp33/django

RUN pip install "djangorestframework==3.3.3" && pip install "requests==2.13.0" && pip install whitenoise
