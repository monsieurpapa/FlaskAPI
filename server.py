from logging import debug
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine  #necessary for configuration of the foreign key constraints

from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import linkedlist  #the module implemented
import hashtable
import binary_search_tree
import random

#THis a BLog API

#app
app = Flask(__name__)

#configuration to use a local file as our database
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///sqlitedb.file" #will contain our entire database (we open it using DBrowser)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=0

#configure sqlite3 to inforce foreign key constraints
@event.listens_for(Engine,"connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db = SQLAlchemy(app) #the SQLAlchemy class connects our app to the ORM
now = datetime.now()


#sqlite : https://sqlitebrowser.org/  : install it

#create the database from the terminal
'''
    >>> from server import db
    >>> db.create_all()
    >>> exit()
'''

#models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete") #cascade is optional but necessary to allow the deletion of a user_id in a foreign table row having the same id
    

#each table class has to inherit the db.Model
class BlogPost(db.Model): 
    __tablename_= "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50))
    body =db.Column(db.String(200))
    date =db.Column(db.Date)
    user_id =db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)


#routes for the API: in order to create functions that correnspond to a route,
# we use the app.route decorater


@app.route("/user",methods=["POST"])  #app.route is a decorator used to define URL rules eg : /user
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message" : "User created"}),200



@app.route("/user/descending_id",methods=["GET"])  
def get_all_users_descending():
    users = User.query.all()   #query.all returns all users in descending order by ID
    all_users_ll = linkedlist.LinkedList() #passing the list of users to a linkedlist data structure

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id":user.id,
                "name":user.name,
                "address": user.address,
                "phone": user.phone

            }
        )

    return jsonify(all_users_ll.to_list()),200


@app.route("/user/ascending_id",methods=["GET"])  
def get_all_users_ascending():
    users = User.query.all()   #query.all returns all users in ascending order by ID
    all_users_ll = linkedlist.LinkedList() #passing the list of users to a linkedlist data structure

    for user in users:
        all_users_ll.insert_at_end(  #because the list of users is already in asceding order
            {
                "id":user.id,
                "name":user.name,
                "address": user.address,
                "phone": user.phone

            }
        )

    return jsonify(all_users_ll.to_list()),200

@app.route("/user/<user_id>",methods=["GET"])  
def get_one_user(user_id):
    users = User.query.all()
    all_users_ll = linkedlist.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id":user.id,
                "name":user.name,
                "address": user.address,
                "phone": user.phone

            }
        )
    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user),200



@app.route("/user/<user_id>",methods=["DELETE"])  
def delete_user(user_id):
     user = User.query.filter_by(id=user_id).first() #check directly in the database
     db.session.delete(user)
     db.session.commit()
     return jsonify({}),200

@app.route("/blog_post/<user_id>",methods=["POST"])  
def create_blogpost(user_id):
     data = request.get_json()

     user = User.query.filter_by(id=user_id).first()
     if not user:
         return jsonify({"message":"user does not exist!"},400) # client sent a bad request
    
     ht = hashtable.HashTable(10)
     ht.add_key_value("title", data["title"])
     ht.add_key_value("body", data["body"])
     ht.add_key_value("date", now)
     ht.add_key_value("user_id",user_id)

     new_blog_post = BlogPost(
         title = ht.get_value("title"),
         body = ht.get_value("body"),
         date = ht.get_value("date"),
         user_id =ht.get_value("user_id")
     )
     db.session.add(new_blog_post)
     db.session.commit()
     return jsonify(
         {"message" : "new blog post created"}),200  #successfull response

     #print hasttable to see what it looks like
    #  print(ht.get_value("title"))
    #  print(ht.get_value("body"))
    #  print(ht.get_value("date"))
    #  print(ht.get_value("user_id"))
     #ht.print_table()

@app.route("/blog_post/<blog_post_id>",methods=["GET"])  #retrieve one blogpost based on its ID
def get_blogpost(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)  # insures that the selection of a blogpost is not based on any order, hence ensures a balanced tree

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id" : post.id,
            "title" : post.title,
            "body":post.body,
            "user_id" :post.user_id,

        })
    
    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message":"post not found"})
    return jsonify(post)

@app.route("/blog_post/<user_id>",methods=["GET"])  
def get_all_blog_posts(user_id):
    pass 

@app.route("/blog_post/<blog_post_id>",methods=["GET"])  
def get_one_blog_post(blog_post_id):
    pass 

@app.route("/blog_post/<blog_post_id>",methods=["DELETE"])  
def delete_blog_post(blog_post_id):
    pass 

if __name__ == "__main__":
    app.run(debug=True)
