from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c35552a8611ba7a0a0057ab541b64bc84bc1dc955ca446a0'

# Note: type 'app.config[..]' as one line, it is split into
# multiple lines in this document to fit on the page
# {USERNAME} and {YOUR_DATABASE} are your Cardiff username
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1887962:Lemontree01@csmysql.cs.cf.ac.uk:3306/c1887962'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from shop import routes






