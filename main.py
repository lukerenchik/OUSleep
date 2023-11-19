
import hashlib
import json
import secrets
import hashlib
import time
import os
import pandas as pd
import chardet
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory, send_file
from forms import signupForm
from piechart import PieHtml
from flask_mail import Mail, Message #use pip install Flask-Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_session import Session # pip install flask_session



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

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

pie_html_instance = PieHtml()

# Load user data from the JSON file.
with open('JSON Data/users.json', 'r') as file:

    users = json.load(file)


@app.route('/')
def index():
    return render_template('preloginhome.html')

# TODO Implement Upload & Download Button in CSS
# Route to download the OUSleep Upload Template
@app.route('/download-template')
def download_template():

    try:
        # Make sure the path to the file is correct and the file exists
        path_to_file = os.path.join(app.root_path, 'JSON Data/OUSleep Upload Template.xlsx')
        return send_file(path_to_file, as_attachment=True)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        
        flash("An Error occurred while trying to upload the file", "error")
        return render_template('homepage.html', username=session['username'])
    
    
    
# Route to upload a file and process it
@app.route('/upload-csv', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash("Error: No file part", "error")
        return render_template('homepage.html', username=session['username'])

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if 'file' not in request.files:
        flash("Error: No file part", "error")
        return render_template('homepage.html', username=session['username'])

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        flash("File is not selected, please select a file", "error")
        return render_template('homepage.html', username=session['username'])

    if file and allowed_file(file.filename):
        # Assuming the username is obtained from a session or a database
        username = session['username']  # Replace with the actual method to get the current user's username

        if not file.filename.endswith('.csv'):
            flash("Invalid file type. Please upload a CSV file", "error")
            return render_template('homepage.html', username=session['username'])

        # Save the uploaded file
        filepath = os.path.join('UploadedFiles', file.filename)  # Set the path to save the file
        file.save(filepath)

        # Process the saved file
        processed_data = process_uploaded_file(filepath)

        # Path to the combined JSON file for all users
        username_file_data_file = os.path.join('UserJsonFiles', 'username_file_data.json')

        # Load existing data or create an empty dictionary
        if os.path.exists(username_file_data_file):
            with open(username_file_data_file, 'r') as file:
                username_file_data = json.load(file)
        else:
            username_file_data = {}

        # Replace the existing data for the current user
        username_file_data[username] = processed_data

        # Write the updated data back to the combined JSON file
        with open(username_file_data_file, 'w') as file:
            json.dump(username_file_data, file, indent=4)

        # Return success response
        flash(f"Data for {username} updated successfully.", "success")
        return render_template('homepage.html', username=session['username'])

    else:
        flash("Invalid file type. Please upload a CSV file", "error")
        return render_template('homepage.html', username=session['username'])
   

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv'}
           

def process_uploaded_file(filepath):
    # Guess the encoding of the file
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    # Read the CSV file with the detected encoding
    df = pd.read_csv(filepath, encoding=encoding)

    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    # Return the processed data
    return data_dict








@app.route('/ForgotPW')
def ForgotPW():

    return render_template('ForgotPW.html')
        
    

@app.route('/Reset_Password', methods=['GET', 'POST'])
def Reset_Password():
    
    input_email = request.form.get('email') 
    
    email_exists = any(user.get('email') == input_email for user in users.values()) # input checks to see if email is apart of .json file
        
    if email_exists: #if email is registered to a user, goes to Reset Password page
        
        session['email'] = input_email
        
        token = s.dumps(input_email, salt='reset-password')
        
        link_to_route = url_for('PWAccess', token=token, _external=True)
        
        msg_title = "Reset Your OU Sleep Account Password"
        
        msg_body = f"Please click <a href='{link_to_route}'>here</a> to go to reset your password. " # The email details
        
        
        

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
        
        input_email = s.loads(token, salt='reset-password', max_age=3600) # 3600 sec. till token expires for link to Reset_Access
        
        
    except SignatureExpired:
        flash("It appears your token has expired, please reinput your email", "error")    
        return redirect(url_for('ForgotPW'))
    return redirect(url_for('Reset_Access'))


@app.route('/Reset_Access')
def Reset_Access():

    return render_template('Reset_Access.html')



@app.route('/ResetPW', methods=['GET', 'POST'])
def ResetPW():
    
    input_email = session.get('email')

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['Confirm_password']
        special_chars = '!@#$%^&*()'

        if new_password == confirm_password:
            if len(new_password) < 6:  #checks if password is more than 6 characters
                flash("Password must be at least 5 characters", "error") 
                return redirect(url_for('Reset_Access'))

            if not any(char in special_chars for char in new_password): #checks if password has a special character
                flash("Password must have a special character", "error")
                return redirect(url_for('Reset_Access'))

            # Retrieve the user's information from users.json
            user_info = None
            for user in users.values():
                if user.get('email') == input_email:
                    user_info = user
                    break

            if user_info is not None:
                # Hash the new password
                new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()

                # Update the user's information with the new password hash
                user_info['password_hash'] = new_password_hash

                # Save the updated user data back to users.json
                with open('users.json', 'w') as file:
                    json.dump(users, file)

                flash("Password successfully updated!", "success")
                return redirect(url_for('ForgotPW'))
            else:
                flash("User not found with the given email", "error")
                return redirect(url_for('Reset_Access'))
        else:
            flash("Passwords do not match, Please try again", "error")
            return redirect(url_for('Reset_Access'))
   

 

    


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

        fig_html = pie_html_instance.get_fig_html()
        scores = pie_html_instance.get_scores_to_display()

        return render_template('homepage.html', username=session['username'], fig_html=fig_html, scores=scores)
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


@app.route('/sleep_stats')
def sleep_stats():

    fig_html = pie_html_instance.get_fig_html()
    scores = pie_html_instance.get_scores_to_display()

    return render_template('sleep_stats.html', username=session['username'], fig_html=fig_html, scores=scores)



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
