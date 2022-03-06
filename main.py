from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy # new
import time
from models import app, Post, db
from serializer import posts_schema

api = Api(app)

post_args = reqparse.RequestParser()
post_args.add_argument('title', type=str, help='title is required', required = True)
post_args.add_argument('content', type=str, help='content is required', required = True)
post_args.add_argument('published', type=bool, default=True)
post_args.add_argument('rating', type=int, help='please check the value type')

# my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I like pizza", "id": 2}]


class Root(Resource):
    def get(self):
        return {"msg":"welcome"}

class Get_post(Resource):
    #getting the whole post
    def get(self):
        posts = Post.query.all()
        data = posts_schema.dump(posts)
        return data

    #adding the post
    def post(self):
        payload = post_args.parse_args()
        new_post = Post(title = payload['title'], content = payload['content'], published = payload['published'])
        db.session.add(new_post)
        db.session.commit()
        data = posts_schema.dump([new_post])
        return data

class Get_post_by_id(Resource):
    #getting individual post
    def get(self, id):
        post = Post.query.filter_by(id=id)
        data = posts_schema.dump(post)
        if not data:
            abort(404, message=f"id {id} doesn't exist")
        return data

    #deleting an individual post
    def delete(self, id):
        deleted_post = Post.query.get(id)
        print("deleted_post", deleted_post)
        if deleted_post == None:
            abort(404, message=f"id {id} doesn't exist")
        db.session.delete(deleted_post)
        db.session.commit()
        return {"message":"post was successfully deleted"}

    #update post by id
    def put(self, id):
        payload = post_args.parse_args()
        updated_post = Post.query.get(id)

        if updated_post == None:
            abort(404, message=f"id {id} doesn't exist")
        else:
            if 'title' in payload:
                updated_post.title = payload['title']
            if 'content' in payload:
                updated_post.content = payload['content']
            if 'published' in payload:
                updated_post.published = payload['published']

        db.session.commit()
        data = posts_schema.dump([updated_post])
        return data


class Latest_post(Resource):
    def get(self):
        latest_post = my_post[len(my_post) -1]
        return {"detail":latest_post}



api.add_resource(Root, "/")
api.add_resource(Get_post, "/post")
api.add_resource(Get_post_by_id, "/post/<int:id>")
api.add_resource(Latest_post, "/post/recent/latest")




if __name__ == "__main__":
    app.run(debug=True)