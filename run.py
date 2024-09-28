from app import create_app, db
from app.auth.models import User

#crar aplicacion dependeiendo la aplicacion de produccion o desareollo 
agro_Logx = create_app("dev")

#envio de contexto inicial del app
with agro_Logx.app_context():
    db.create_all()
    if not User.query.filter_by(user_name = "test").first():
        User.create_user(
            user = "test",
            phone = "3112456789",
            email = "test-testing@test.com",
            password = "test**123"
        )

#ejecusion de la app
if __name__ == '__main__':
    agro_Logx.run()