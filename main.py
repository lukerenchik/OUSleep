from flask import Flask, render_template, request, redirect, url_for, session, flash
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


@app.route('/ForgotPW')
def ForgotPW():
    
    return render_template('ForgotPW.html')
  

    


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        dob = request.form.get('dob')

        # Check if the password and confirm_password match.
        if password != confirm_password:
            flash("Passwords do not match, please try again.", "error")
            return redirect(url_for('signup'))

        # Check if the username already exists.
        if username in users:
            print("Username already exists, please choose another one.", "error")
            return redirect(url_for('signup'))

        # Hash the password.
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Save user data to users.json.
        users[username] = {
            'email': email,
            'password_hash': password_hash,
            'dob': dob
        }

        with open('users.json', 'w') as file:
            json.dump(users, file)

        print("Account created successfully. You can now log in.", "success")
        return redirect(url_for('index'))
    return render_template('signup.html')


# Password hashing function (you should use a secure library for this).
def check_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password


if __name__ == '__main__':
    # print(hashlib.sha256("password".encode()).hexdigest())
    app.run(debug=True)
