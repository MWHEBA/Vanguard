import os
import sys
import gc

# Add the project directory to the sys.path
PROJECT_DIR = '/home/vanguard/vanguard_prod'
sys.path.insert(0, PROJECT_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Reduce garbage collection threshold for shared hosting
gc.set_threshold(700, 10, 10)

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
