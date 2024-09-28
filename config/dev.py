DEBUG = True
SECRET_KEY = 'secret'
# SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/agrologix"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/agrologix"
SQLALCHEMY_TRACK_MODIFICATIONS = False