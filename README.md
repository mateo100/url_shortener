# url_shortener

1. Create virutal environemnt (venv)
2. pip install -r requirements.txt
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver

### endpoints
1. [POST] /shorten/

body: 
{
  "url": <WEBSITE_URL>
}

2. [GET] /mateok/<SHORT_URL>/
