from flask import Flask

# initialise app 
app = Flask(__name__)

# Avoid circular import ?
from app import routes