from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort
from random import randrange
import psycopg2
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisthesecretkey"
api = Api(app)

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = "localhost", database="learning_project", user="postgres", password="461775")

        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("connecting to database is successful")
        break
    except Exception as e:
        print("Database connection failed")
        print("error", e)
        time.sleep(2)

post_args = reqparse.RequestParser()
post_args.add_argument('title', type=str, help='title is required', required = True)
post_args.add_argument('content', type=str, help='content is required', required = True)
post_args.add_argument('published', type=bool, default=True)
post_args.add_argument('rating', type=int, help='please check the value type')

my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i in range(len(my_post)):
        if my_post[i]["id"] == id:
            return i

class Root(Resource):
    def get(self):
        return {"message":"welcome"}

    def post(self):
        payload = post_args.parse_args()
        print("payload", payload.rating)
        return {"new_post":payload}

class Get_post(Resource):
    #getting the whole post
    def get(self):
        # Execute a query
        cur.execute("""SELECT * FROM posts""")
        # Retrieve query results
        data = cur.fetchall()
        my_post = {}
        for i in data:
            my_post["id"]           = i[0]
            my_post["title"]        = i[1]
            my_post["content"]      = i[2]
            my_post["published"]    = i[3]
            my_post["created_at"]   = str(i[4])
        return {"data":my_post}

    #adding the post
    def post(self):
        payload = post_args.parse_args()
        cur.execute("INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)", (payload['title'], payload['content'], payload['published']))
        conn.commit()
        return {"data":"created post"}, 201

class Get_post_by_id(Resource):
    #getting individual post
    def get(self, id):
        # Execute a query
        cur.execute(f"SELECT * FROM posts where id = {id}")
        # Retrieve query results
        data = cur.fetchone()
        print("data", data)
        my_post = {}
        my_post["id"]           = data[0]
        my_post["title"]        = data[1]
        my_post["content"]      = data[2]
        my_post["published"]    = data[3]
        my_post["created_at"]   = str(data[4])
        if not data:
            abort(404, message=f"id {id} doesn't exist")

        return {"post_detail":my_post}

    #deleting an individual post
    def delete(self, id):
        cur.execute(f"DELETE FROM posts where id = {id} RETURNING *")
        deleted_post = cur.fetchone()
        conn.commit()

        if deleted_post == None:
            abort(404, message=f"id {id} doesn't exist")
        return {"message":"post was successfully deleted"}

    #update post by id
    def put(self, id):
        payload = post_args.parse_args()
        cur.execute("UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *", (payload['title'], payload['content'], payload['published'], id))
        updated_post = cur.fetchone()
        conn.commit()

        if updated_post == None:
            abort(404, message=f"id {id} doesn't exist")
        return {"message":"the post has been updated"}, 200


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