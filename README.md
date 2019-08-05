# django-chat
Install python:

        https://www.python.org/downloads/
        
For Windows:
        
        https://visualstudio.microsoft.com/ru/downloads/ install python C++ compiler
        pip install --upgrade setuptools
        
Clone repo:
        
        git clone https://github.com/TomoeFox/django-chat.git
        
Python dependencies:

    pip install django
    
    pip install pathlib
    
    pip install django-bootstrap3
  
    pip install -U channels
  
    pip install asgiref==2.3.0

Download and install Redis:

    Linux:
        https://redis.io/download
    
    Windows:
        https://redislabs.com/ebook/appendix-a/a-3-installing-on-windows/a-3-2-installing-redis-on-window/
  
Then go to django-chat main folder and start django server using command: 
    
    python manage.py runserver
Shut down server using CTRL+C and
After server is started go to 127.0.0.1:8000 and login as Test user, credentials for it: 
    
    Login: Test, Password: Test
