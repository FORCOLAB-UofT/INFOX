from app import create_app
from app.celery import celery

# CONFIGURE_MODE = "production"

CONFIGURE_MODE = "default"

app = create_app(CONFIGURE_MODE)
app.app_context().push()
