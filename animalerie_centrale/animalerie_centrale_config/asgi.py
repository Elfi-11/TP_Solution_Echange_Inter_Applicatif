import os
from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "animalerie_centrale_config.settings")
application = get_asgi_application()
