import hashlib
import json
import secrets
import hashlib
import time

from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import signupForm
from piechart import pie_html
from flask_mail import Mail, Message #use pip install Flask-Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired



app = Flask(__name__, template_folder="templates", static_folder="static")


app.config['SECRET_KEY'] = "439D699B2F1C8BCAD6616AC339CA4"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'noreplyousleep@gmail.com'
app.config['MAIL_PASSWORD'] = 'uznc yptb opfd bdaj'
app.config['MAIL_DEFAULT_SENDER'] = 'noreplyousleep@gmail.com'


mail = Mail(app)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key.s

s = URLSafeTimedSerializer('439D699B2F1C8BCAD6616AC339CA4')



# Load user data from the JSON file.
with open('JSON Data/users.json', 'r') as file:

    users = json.load(file)


@app.route('/')
def index():
    return render_template('preloginhome.html')


@app.route('/ForgotPW')
def ForgotPW():

    return render_template('ForgotPW.html')
        
    

@app.route('/Reset_Password', methods=['GET', 'POST'])
def Reset_Password():
    
    input_email = request.form.get('email') 
    
    email_exists = any(user.get('email') == input_email for user in users.values()) # input checks to see if email is apart of .json file
        
    if email_exists: #if email is registered to a user, goes to Reset Password page
        
        token = s.dumps(input_email, salt='reset-password')
        
        link_to_route = url_for('Reset_Access', token=token, _external=True)
        
        msg_title = "Reset Your OU Sleep Account Password"
        
        msg_body = f"Please click <a href='{link_to_route}'>here</a> to go to reset your password. "
        
        
        

        msg = Message(msg_title, html=msg_body, recipients=[input_email])
        
        
        try:
            mail.send(msg)
            flash("Reset Request Email Has been sent! Please check your email!", "success")
            return redirect(url_for('ForgotPW'))
    
        except Exception as e:
            flash("There was a problem in sending the Reset Password link, Please try again", "error")    
        return redirect(url_for('ForgotPW'))
        
        

         
    
     
    
    else:
        flash("The Email Address Entered is not regeistered with a user, please try again", "error")    
        return redirect(url_for('ForgotPW'))
        
    
    
   
    
@app.route('/PWAccess/<token>')
def PWAccess(token):
    try:
        
        input_email = s.loads(token, salt='reset-password', max_age=200)
        
        
    except SignatureExpired:
        flash("It appears your token has expired, please reinput your email", "error")    
        return redirect(url_for('ForgotPW'))
    return redirect(url_for('Reset_Access'))


@app.route('/Reset_Access')
def Reset_Access():

    return render_template('Reset_Access.html')





    


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username exists.
    if username in users:
        # Hash the provided password for comparison.
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check if the provided password matches the stored password_hash.
        if check_password(password, users[username]['password_hash']):
            # Successful login, set session variables or cookies as needed.
            session['username'] = username
            return redirect(url_for('homepage'))

    # Invalid login, display an error message.
    flash("Invalid username or password", "error")
    return redirect(url_for('index'))


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
    form = signupForm()
    if not form.validate_on_submit():
        return render_template('signup.html', title='Sign Up', form=form)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')

        # Check if the username already exists.
        if username in users:
            flash("Username already exists, please choose another one.", "error")
            return redirect(url_for('signup'))
        
        elif email in [user_data.get('email') for user_data in users.values()]: # Added so that there will be no duplicate emails in sign up
            flash("Email already associated with an account, please use another email.", "error")
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

    return render_template('signup.html',title='Sign Up',form=form)


# Password hashing function (you should use a secure library for this).
def check_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

def generate_reset_token():
    # Generate a random and secure token (32 bytes)
    token = secrets.token_hex(16)
    # Include a timestamp to track the token's expiration (e.g., 1 hour from now)
    timestamp = int(time.time()) + 3600  # 3600 seconds = 1 hour
    # Combine the token and timestamp
    reset_token = f"{token}.{timestamp}"
    
    return reset_token


    


if __name__ == '__main__':
    # print(hashlib.sha256("password".encode()).hexdigest())
    app.run(debug=True)
