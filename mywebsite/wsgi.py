"""
WSGI config for mywebsite project.
Production-ready for PythonAnywhere.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

# Get Django application
django_application = get_wsgi_application()

# Wrap with WhiteNoise for production
def application(environ, start_response):
    app = django_application
    # Check if we're in production
    if os.environ.get('DJANGO_DEBUG', 'True').lower() == 'false':
        try:
            from whitenoise import WhiteNoise
            app = WhiteNoise(app)
        except ImportError:
            pass
    
    return app(environ, start_response)