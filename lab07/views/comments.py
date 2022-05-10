from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post
from views import can_view_post

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # TODO: create a new "Comment" based on the data posted in the body 
        ## Create a new comment associated with the specified pot
        ## post_id: int (required)
        ## text: string (required)
        ## Response Type: Comment object
        body = request.get_json()
        print(body)
        # ------------------------ CODE START HERE ------------------------ #
        ## Check if input did not meet required 2 itemss:
        if len(body) < 2:
            return Response(json.dumps({"message": "'text' and 'post_id' are required"}), mimetype="application/json", status=400)
        ## Check if post_id is int:
        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({"message": "the given post_id is invalid"}), mimetype="application/json", status=400)
        ## Check if post exists in all posts
        if Post.query.get(post_id) is None:
            return Response(json.dumps({"message": "post_id={0} is invalid.".format(post_id)}), mimetype="application/json", status=404)
        ## Check if the user is authorized (followed by the current user)
        ## Use can_view_post()
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({"message": "You cannot view this post: {0}.".format(post_id)}), mimetype="application/json", status=404)
        
        text = body.get('text')
        user_id = self.current_user.id
        
        new_comment = Comment (
            text,
            user_id,
            post_id
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        # ----------------------------------------------------------------- #

        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        ## Delete a comment
        ## You can ONLY delete a comment that you created
        # print(id)
        # ------------------------ CODE START HERE ------------------------ #
        ## Check if the id is int
        try:
            id = int(id)
        except:
            return Response(json.dumps({"message": "the given id is invalid."}), mimetype="application/json", status=404)
        ## Check if the id exists and sent out by current user
        if Comment.query.get(id) is None or Comment.query.get(id).user_id != self.current_user.id:
            return Response(json.dumps({"message": "id={0} does not exist.".format(id)}), mimetype="application/json", status=404)
        # print(Comment.query.get(id).user_id)
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps({"message": "Comment id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)
        # ----------------------------------------------------------------- #


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
