# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *  # noqa: F403,F401


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'khaled_project_peter_emil_2019',
        'USER': 'peter',
        'PASSWORD': 'peter',
        'HOST': 'localhost',
        'PORT': 3306
    }
}
