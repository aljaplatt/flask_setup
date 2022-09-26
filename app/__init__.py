from flask import Flask

# initialise app 
app = Flask(__name__)

# Avoid circular import ? - importing blueprints
from app import routes