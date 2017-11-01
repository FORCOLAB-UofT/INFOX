import os

from flask import Flask
from app import create_app
from flask_script import Manager, Shell

CONFIGURE_MODE = "default"

print "configure mode = ", CONFIGURE_MODE
# os.system('mango')
app = create_app(CONFIGURE_MODE)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
