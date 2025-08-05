import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'capupec',
        'USER': 'administrador',
        'PASSWORD': 'tesis123',
        'HOST': '172.20.24.40',
        'PORT': '5432',  
    }
}
