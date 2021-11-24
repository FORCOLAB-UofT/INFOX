from app import celery, create_app

# CONFIGURE_MODE = "production"

CONFIGURE_MODE = "default"

app = create_app(CONFIGURE_MODE)
app.app_context().push()
