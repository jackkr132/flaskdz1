from flask import jsonify, request
from flask.views import MethodView
import app
import errors
from models import User, Post, return_all_posts

from validate_schema import POSTS_SCHEMA
from validators import validate


class PostsView(MethodView):

    def get(self, post_id=None):
        getting = return_all_posts()
        return jsonify(getting)

    def retrieve(self, post_id=None):
        post = Post.by_id(post_id)
        if not post:
            raise errors.NotFound
        return jsonify(post)

    @validate("json", POSTS_SCHEMA)
    def post(self):
        post_positions = [POSTS_SCHEMA["properties"].keys()]
        if request.json.keys() not in post_positions:
            raise errors.BadLuck
        post = Post(**request.json)
        post.add()
        return jsonify(post.to_dict())

    @validate("json", POSTS_SCHEMA)
    def patch(self, post_id=None):
        post_positions = [POSTS_SCHEMA["properties"].keys()]
        if request.json.keys() not in post_positions:
            raise errors.BadLuck
        post = Post.by_id(post_id)
        post.header = request.json["header"]
        post.text = request.json["text"]
        post.owner_id = request.json["owner_id"]
        post.add()
        return jsonify(post.to_dict())

    def delete(self, post_id=None):
        get = Post.by_id(post_id)
        if not get:
            raise errors.NotFound
        Post.query.filter_by(id=post_id).delete()
        app.db.session.commit()
        return jsonify({"status": "deleted"})


app.app.add_url_rule('/posts', view_func=PostsView.as_view('posts_get'), methods=['GET', ])
app.app.add_url_rule('/posts/<int:post_id>', view_func=PostsView.as_view('posts_retrieve'), methods=['GET', ])
app.app.add_url_rule('/posts/', view_func=PostsView.as_view('posts_post'), methods=['POST', ])
app.app.add_url_rule('/posts/<int:post_id>/', view_func=PostsView.as_view('posts_patch'), methods=['PATCH', ])
app.app.add_url_rule('/posts/<int:post_id>/', view_func=PostsView.as_view('posts_delete'), methods=['DELETE', ])
