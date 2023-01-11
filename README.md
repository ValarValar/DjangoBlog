# DjangoBlog
## Summary
Showcase pet-project with Django/DjagoRestAPI implementation of Blog application. Main purpose of it is to store somewhere my self-development process.
## Technology stack
Django, DjangoRestAPI 
virtualization -> Docker/docker-compose     
db -> Postgresql    
documentation -> Drf-spectacular  
testing -> unittest(drf)
This project is created for education, so i decided to leave for now here .env.dev file and DebugToolbar is still turned on
## Models
Profile -> proxy for default user model to store data connected with User instead of changing default User model.
post_save signal autocreating
[other models declaration](https://github.com/ValarValar/DjangoBlog/blob/master/blog/api/models.py)
## Project contents  
* Registration enpoints, authentication via jwt (basic model.auth.User и SimpleJwt)
* Post creation endpoint. Require Authentication.
* User list endpoint. Allows to order by username and posts_count.
* List of user's detailed posts. Ordered by post creation time. Starting with the newest ones.
* Subscribe/unsubscribe endpoint. Require authentication.
* Feed endpoint provides you posts of users you subcribed on.
* Endpoint allows to mark or unmark post as seen.
Manual containing usage of API endpoinst u can find at swagger endpoint after setting up project.
## Setup
reminder: don't forger to configure your interpreter and activate venv.   
activate venv    
pip install docker    
docker-compose up -d --build    
docker-compose exec django_blog_app python manage.py makemigrations    
docker-compose exec django_blog_app python manage.py migrate    
docker-compose exec django_blog_app python manage.py createsuperuser --username admin --email admin@mail.ru    
docker-compose exec django_blog_app python manage.py test .     
docker-compose up -d --build     
