# Import flask class
from flask import Flask

# initialise app - creates the Flask instance class, configures the application. Allows you to access global objectsfrom the scope of the package
app = Flask(__name__)

# Avoid circular import ? - importing blueprints
from app import routes

# if __name__ == "__main__":
#     app.run(debug=True)