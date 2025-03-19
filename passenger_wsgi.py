import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + "/core")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
