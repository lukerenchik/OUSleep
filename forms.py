from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from datetime import datetime, timedelta

class signupForm(FlaskForm):
    username = StringField(label='Username:',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField(label='Email:',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password:',id='password',validators=[DataRequired(),Length(min=6,max=16)])
    confirm_password = PasswordField(label='Confirm Password:',id='confirm_password',validators=[DataRequired(),EqualTo('password')])
    dob = DateField(label='Date of Birth:',id='dob',validators=[DataRequired()])

    def validate_dob(self, field):
        dob_formatted = datetime.strptime(field.data.strftime("%Y-%m-%d"), "%Y-%m-%d")
        long_ago = datetime.now() - timedelta(days=365 * 18)
        print(dob_formatted)
        print(long_ago)
        if not dob_formatted <= long_ago:
            raise ValidationError('Date of Birth must be more than 18 years ago')

    signup = SubmitField(label='Sign Up')