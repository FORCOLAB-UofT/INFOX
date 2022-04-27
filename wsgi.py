from flask import Flask
from app import create_app

# TODO: make configuration mode auto detectable for production versus development
CONFIGURE_MODE = "production"
#CONFIGURE_MODE = "default"

app = create_app(CONFIGURE_MODE)
