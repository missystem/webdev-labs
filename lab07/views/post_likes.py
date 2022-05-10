from flask import Response, request
from flask_restful import Resource
from models import LikePost, db, Post
import json
from views import can_view_post

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # TODO: create a new "like_post" based on the data posted in the body 
        ## Create a like
        ## post_id: int (required)
        ## LikePost object
        body = request.get_json()
        # print(body)
        # ------------------------ CODE START HERE ------------------------ #
        ## Check if post_id is int:
        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({"message": "the post_id is invalid."}), mimetype="application/json", status=400)
        ## Check if post exists in all posts
        if not Post.query.get(post_id):
            return Response(json.dumps({"message": "post_id={0} does not exist.".format(post_id)}), mimetype="application/json", status=404)
        ## Check if the user is authorized (followed by the current user)
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({"message": "You cannot view this post."}), mimetype="application/json", status=404)
        ## Check if post_id exists
        lp_query = LikePost.query.filter_by(user_id=self.current_user.id).all()
        lp_post_ids = [lp.post_id for lp in lp_query]
        if post_id in lp_post_ids:
            return Response(json.dumps({"message": "You already liked post_id={0}.".format(post_id)}), mimetype="application/json", status=400)

        user_id = self.current_user.id
        ## Like a new post
        liked = LikePost (user_id, post_id)
        ## add to database and commit
        db.session.add(liked)
        db.session.commit()
        # ----------------------------------------------------------------- #
        return Response(json.dumps(liked.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        ## DELETE "like_post" where "id"=id
        ## You can ONLY delete a "like" that you created
        # print(id)
        # ------------------------ CODE START HERE ------------------------ #
        ## query all post_likes by current user
        lp_query = LikePost.query.filter_by(user_id=self.current_user.id).all()
        lp_ids = [lp.id for lp in lp_query]
        ## if id in current user's post_likes
        if id in lp_ids:
            LikePost.query.filter_by(id=id).delete()
            ## commit changes to the database
            db.session.commit()
            return Response(json.dumps({"message": "You have successfully unliked post id={0}.".format(id)}), mimetype="application/json", status=200)
        # ----------------------------------------------------------------- #
        return Response(json.dumps({"message": "id={0} is invalid.".format(id)}), mimetype="application/json", status=404)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
