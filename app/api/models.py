# -*- coding: utf-8 -*-
from flask import jsonify, g, request
from flask_restful import Resource, Api, reqparse

from . import api

restful_api = Api(api)

class RepoApi(Resource):
    """
    RESTful API:
        获取所有微博以及发布微博
    """

    def __init__(self):
        pass
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('post', type=str, required=True,
                                 help='No post provided', location='json')
        super().__init__()
        """

    def get(self):
        return jsonify({'repo_list': ['aaa','bbb']})
        """
        page = request.args.get('page', 1, type=int)
        pagination = Post.query.paginate(page, error_out=False)
        posts = pagination.items
        if posts is None:
            return Error.page_not_found
        return jsonify(
            {'post': [post.to_json() for post in posts]})
        """

    def post(self):
        return {'status': 200}

class RepoByNameApi(Resource):
    """
    RESTful API:
        通过 id 获取微博
    """

    def get(self, name):
        return jsonify({'repo':name})
        """
        post = Post.query.filter_by(id=id).first()
        if post is None:
            return Error.page_not_found
        return jsonify(post.to_json())
        """

class ForkApi(Resource):
    """
    RESTful API:
        获取所有Fork
    """

    def get(self):
        return jsonify({"fork_list":["ccc","ddd"]})
        """
        page = request.args.get('page', 1, type=int)
        pagination = Comment.query.paginate(page, error_out=False)
        comments = pagination.items
        if comments is None:
            return Error.page_not_found
        return jsonify({
            'comment': [comment.to_json() for comment in comments],
            'totalCommentsCount': pagination.total
        })
        """


class ForkByNameApi(Resource):
    """
    RESTful API:
        通过 Name 获取Fork
    """

    def get(self, name):
        return jsonify({'fork':name})
        """
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            return Error.page_not_found
        return jsonify(comment.to_json())
        """


restful_api.add_resource(RepoApi, '/repo')
restful_api.add_resource(RepoByNameApi, '/repo/<string:name>')

restful_api.add_resource(ForkApi, '/fork')
restful_api.add_resource(ForkByNameApi, '/fork/<string:name>')
