from importlib.abc import ResourceReader
from flask import Response, request
from flask_restful import Resource
from models import LikeComment, db, Post, Comment
import json
from views import can_view_post


class CommentLikesListEndpoint(Resource):
    
    def __init__(self, current_user):
        self.current_user = current_user
        
    def post(self):
        ## TODO: CREATE a new "like_comment" based on the data posted in the body
        body = request.get_json()
        print(body)
        # ------------------------ CODE START HERE ------------------------ #
        ## Check if comment_id is int:
        try:
            comment_id = int(body.get('comment_id'))
        except:
            return Response(json.dumps({"message": "the given comment_id is invalid."}), mimetype="application/json", status=400)
        ## if this comment exists in comment table
        if Comment.query.get(comment_id) is None:
            return Response(json.dumps({"message": "Comment id={0} does not exist.".format(comment_id)}), mimetype="application/json", status=404)
        
        ## Check if the user can view this comment
        ## Check if the user is authorized --> can view this post
        post_id_comment_join = (
            db.session
            .query(Post.id, Comment.id, LikeComment.id)
            .join(Comment, Comment.post_id == Post.id)
            .join(LikeComment, LikeComment.comment_id == Comment.id)
            .filter(Comment.id == 5)
            .all()
        )
        post_id = post_id_comment_join[0][0]
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({"message": "You cannot view this post: {0}.".format(post_id)}), mimetype="application/json", status=404)
        ## if already liked the comment
        lc_query = LikeComment.query.filter_by(user_id=self.current_user.id).all()
        lc_comment_ids = [lc.comment_id for lc in lc_query]
        if comment_id in lc_comment_ids:
            return Response(json.dumps({"message": "You already liked comment id={0}.".format(comment_id)}), mimetype="application/json", status=400)

        ## Check if this comment exists in this post:
        user_id = self.current_user.id
        ## Like a new comment
        new_likes = LikeComment(user_id, comment_id)
        ## add to database and commit
        db.session.add(new_likes)
        db.session.commit()
        return Response(json.dumps(new_likes.to_dict()), mimetype="application/json", status=201)
        # ----------------------------------------------------------------- #


class CommentLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def delete(self, id):
        ## DELETE the "like_comment" where "id"=id
        ## You can ONLY delete a "like" that you created
        # ------------------------ CODE START HERE ------------------------ #
        print(id)
        lc_query = LikeComment.query.filter_by(user_id=self.current_user.id).all()
        lc_ids = [lc.id for lc in lc_query]
        if id in lc_ids:
            LikeComment.query.filter_by(id=id).delete()
            ## commit changes to the database
            db.session.commit()
            return Response(json.dumps({"message": "You have successfully unliked comment id={0}.".format(id)}), mimetype="application/json", status=200)
        return Response(json.dumps({"message": "id={0} is invalid.".format(id)}), mimetype="application/json", status=404)
        # ----------------------------------------------------------------- #

    
def initialize_routes(api):
    api.add_resource(
        CommentLikesListEndpoint,
        '/api/comments/likes',
        '/api/comments/likes/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        CommentLikesDetailEndpoint,
        '/api/comments/likes/<int:id>',
        '/api/comments/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
