# from the app package/folder, import the app function
from app import app

# route / view is a decorator, pass in url 
@app.route("/")
# we return something by writing a function 
def index():
    return "Hello World"

app.route("/about")
def about():
    return "<h1 style='color: red'>About! </h1> "