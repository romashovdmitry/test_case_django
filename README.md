# Project
Test task for ATrucks by Python Backend Developer Romashov Dmitry

## Stack of technologies: 
- Django, Django ORM
- pandas for reading CSV
- requests for download CSV
- beautifulsoup for searching CSV in DOM
- DRF for creating API 
- HTML, Bootstrap for UI
- crontab for scheduled rewriting CSV
- Docker for runing

# How To Run on local machine

1. git clone https://github.com/romashovdmitry/test_case_django.git
2. docker-compose up

Because of downloading CSV happens on schedule, you can run it by yourself by next way:

3. docker ps
4. Get container id of django_test_case
5. docker exec -t -i CONTAINER_ID bash
6. python3 manage.py update_csv
7. Wait about 2 minutes. And stalk for location of your's ex on http://127.0.0.1:8000/
