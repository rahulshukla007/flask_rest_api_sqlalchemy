from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP # new

app = Flask(__name__)
SQLALCHEMY_DATABASE_URL ='postgresql://postgres:461775@localhost/learning_project'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL # new
db = SQLAlchemy(app) # new

class Post(db.Model):
    __tablename__ = "posts"
    id          = db.Column(db.Integer, primary_key=True, nullable=False)
    title       = db.Column(db.String, nullable=False)
    content     = db.Column(db.String,  nullable=False)
    published   = db.Column(db.Boolean, server_default = 'True', nullable=False)
    created_at  = db.Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))


    def __init__(self, title, content, published):
        self.title = title
        self.content = content
        self.published = published


    