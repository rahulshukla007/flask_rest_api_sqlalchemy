from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # new
from models import Post
app = Flask(__name__)
SQLALCHEMY_DATABASE_URL ='postgresql://postgres:461775@localhost/learning_project'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL # ne
ma = Marshmallow(app) # new

class PostSchema(ma.Schema):
    class Meta:
        fields = ("title", "content", "published")
        model = Post

posts_schema = PostSchema()
posts_schema = PostSchema(many=True)