from flask import render_template, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm
from app.auth import authentication
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user

@authentication.route("/")
def index ():
    return render_template("index.html")

@authentication.route("/register", methods = [ "GET", "POST" ])
def register_user():
    """validacion de si esta autenticado el usuario o no o si se encurntra resitrado en la base de datos"""
    if current_user.is_authenticated:
        flash("you are already logged in the sistem")
        return redirect(url_for("authentication.index"))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        User.create_user(
            user = form.name.data,
            phone = form.phone.data,
            email = form.email.data,
            password = form.password.data
        )
        flash("Registratiuon Done ...")  
              
        return redirect(url_for("authentication.log_in_user"))
    return render_template("register.html", form = form)

@authentication.route("/login", methods=["GET","POST"])
def log_in_user():
    """autenticacion de login de usuarios"""
    
    if current_user.is_authenticated:
        flash("you are already logged in the sistem")
        return redirect(url_for("authentication.index"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_email = form.email.data).first()
        
        if not user or not user.check_password(form.password.data):
            flash("Invalid credentials...")
            return redirect(url_for("authentication.log_in_user"))
        
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for("authentication.index"))
    
    return render_template("login.html", form = form)

@authentication.route("/compras")
@login_required
def compras():
    return render_template("compras.html")

@authentication.route("/graficas")
@login_required
def graficas():
    return render_template("graficos.html")

@authentication.route("/IA")
@login_required
def ia():
    return render_template("ia.html")

@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():
    """cerar sesion del usuario requiriendo estar logeado"""
    logout_user()
    return redirect(url_for("authentication.log_in_user"))

@authentication.app_errorhandler(404)
def page_not_fount(error):
    """si el usuario no encuentra una pagina no existente"""
    return render_template('404.html'), 404