# Import the render_template function from Flask

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    # This function looks for the file in the 'templates' folder
    return render_template('index.html')