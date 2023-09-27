from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'  # Replace with a secure secret key.s

# Load user data from the JSON file.
with open('users.json', 'r') as file:
    users = json.load(file)


@app.route('/')
def index():
    return render_template('preloginhome.html')

@app.route('/forgotpw')
def forgotpw():
    return render_template('forgotpw.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username exists and the password is correct.
    if username in users and check_password(password, users[username]['password_hash']):
        # Successful login, set session variables or cookies as needed.
        session['username'] = username
        return redirect(url_for('homepage'))
    else:
        # Invalid login, handle accordingly (e.g., display an error message).
        return "Invalid username or password"


@app.route('/homepage')
def homepage():
    # Check if the user is logged in (session or cookie).
    if 'username' in session:
        return render_template('homepage.html', username=session['username'])
    else:
        # Redirect to the login page or display a message.
        return redirect(url_for('index'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


# Password hashing function (you should use a secure library for this).
def check_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password


if __name__ == '__main__':
    app.run(debug=True)
