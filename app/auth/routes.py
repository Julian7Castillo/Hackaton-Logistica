from flask import render_template, flash, redirect, url_for, Flask, Response
from app.auth.forms import RegistrationForm, LoginForm, BuyForm
from app.auth import authentication
from app.__init__ import excel_Train, excel_Test
from app.auth.models import User, Compras
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

@authentication.route("/perfil")
@login_required
def perfil():
    
    user_id = current_user.id,
    user_name = current_user.user_name,
    user_phone = current_user.user_phone,
    user_email = current_user.user_email,
    create_date = current_user.create_date
        
    data = {
        "user_id" : user_id,
        "user_name" : user_name,
        "user_phone" : user_phone,
        "user_email" : user_email,
        "create_date" : create_date
    }

    return render_template('user.html', data=data)  # Pasar los usuarios a la plantilla

@authentication.route("/compras", methods=["GET","POST"])
@login_required
def compras():
    
    form = BuyForm()
    
    cards = Compras.get_all_buys()  # Obtener todas las compras
    
    if form.validate_on_submit():
        
        Compras.create_compra(
            suministro = form.suministro.data,
            direccion = form.direccion.data,
            departamento = form.departamento.data,
            asunto = form.asunto.data
        )
        flash("Compra realizada ...")  
              
        return redirect(url_for("authentication.compras"))
    
    data = {
        "form":form ,
        "cards":cards
    }
    return render_template("compras.html", data = data)

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


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io


@authentication.route("/graficas")
@login_required
def graficas():
    
    df = pd.read_csv(excel_Train, delimiter=';')
    
    df.drop(['ID'], axis = 1,inplace=True)

    table_html = df.describe().to_html(classes='table table-striped')  # Añadir clases CSS si es necesario

    # Renderizarlo en la plantilla HTML
    return render_template("graficos.html",table_html=table_html)
    
@authentication.route("/graficar")
def grafiacar():
    df = pd.read_csv(excel_Train, delimiter=';')
    
    df = pd.read_csv(excel_Train, delimiter=';')
    
    # Agrupar por tipo, calcular el promedio de violaciones, ordenar y seleccionar el top 10
    top_10 = df.groupby('Type')['SectionViolations'].mean().sort_values(ascending=False).head(10)

    # Crear la gráfica de barras
    top_10.plot(kind='bar', title='Top 10 Promedio por Tipo de Instalación con más violaciones de calidad')

    output = io.BytesIO()
    plt.savefig(output, format='png')
    output.seek(0)
    
    # Renderizarlo en la plantilla HTML
    return Response(output.getvalue(), mimetype='image/png')