from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User

def email_exists(form, field):
    email = User.query.filter_by(user_email = field.data).first()
    if email:
        raise ValidationError("Email alredy exists. !!!")
        
class RegistrationForm(FlaskForm):
    """clase de validacion de campos email y password del registrp"""
    name = StringField("Name", validators = [DataRequired(), Length(4,16, message="Between 4 to 16 characters")])
    phone = StringField("phone", validators = [DataRequired(), Length(10, message="11 characters")])
    email = StringField("Email", validators = [DataRequired(), Email(), email_exists])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm = PasswordField("Confirm", validators = [DataRequired(), EqualTo("Password", message="Password must match !!!")])
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    """Creacion autiomatica del formulario indicando campos del login """
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    stay_loggedin = BooleanField("Remenber Me!")
    submit = SubmitField("login")
        
class BuyForm(FlaskForm):
    """Creacion autiomatica del formulario indicando campos del la compra """
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    stay_loggedin = BooleanField("Remenber Me!")
    submit = SubmitField("login")