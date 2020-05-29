from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField

class User_registration(FlaskForm):
    
    user_name = StringField("user_name: ")
    user_surname = StringField("user_surname: ")  
    user_age = StringField("user_age: ")
    user_mail = StringField("user_mail: ") 
    user_login = StringField("login: ")
    user_pass = PasswordField("password: ")
    submit = SubmitField("submit")

class Add_prediction(FlaskForm):
    
    prediction_description =  StringField("your prediction: ")
    submit1 = SubmitField("submit")

class Add_numerology_date(FlaskForm):
    
    numerology_date = StringField("numerology_date: ")
    numerology_description = StringField("numerology_description: ")    
    submit2 = SubmitField("submit")

class sign_in(FlaskForm):
    
    login = StringField("login: ")
    user_pass = PasswordField("password: ")
    submit = SubmitField("OK")