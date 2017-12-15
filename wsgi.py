from flask import Flask
from app import create_app

CONFIGURE_MODE = "production"

app = create_app(CONFIGURE_MODE)
