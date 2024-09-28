from datetime import datetime
from app import db, Bcrypt 
from app import login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_phone = db.Column(db.String(11))
    user_email = db.Column(db.String(60), unique=True, index = True)
    user_password = db.Column(db.String(80))
    create_date = db.Column(db.DateTime, default=datetime.now)
    
    def check_password(self, password):
        return Bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_user(cls, user, phone, email, password):
        user = cls(user_name = user,
                   user_phone = phone,
                   user_email = email,
                   user_password = Bcrypt.generate_password_hash(password).decode("utf-8")
        )
        
        db.session.add(user)
        db.session.commit()
        return user

@login_manager.user_loader
def load_user(id):
    """retorna el id del usuario validando si esta activo o no osea logeado"""
    return User.query.get(int(id))