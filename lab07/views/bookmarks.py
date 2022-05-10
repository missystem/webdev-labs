from flask import Response, request
from flask_restful import Resource
from models import Bookmark, bookmark, db, Post, User
from views import can_view_post
import json

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        ## TODO: GET all bookmarks owned by the current user
        ## Should display all of the current user's bookmarks (saved posts)
        ## Use the Bookmark data model to get this information
        # ------------------------ CODE START HERE ------------------------ #
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        # print(bm_query)
        bookmarks_json = [bm.to_dict() for bm in bookmarks]
        # ----------------------------------------------------------------- #
        return Response(json.dumps(bookmarks_json), mimetype="application/json", status=200)

    def post(self):
        ## TODO: CREATE a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        # print(body)
        # ------------------------ CODE START HERE ------------------------ #
        ## Check if post_id is int
        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({"message": "the given post_id is invalid."}), mimetype="application/json", status=400)
        ## Check if post exists in all posts
        if not Post.query.get(post_id):
            return Response(json.dumps({"message": "post_id={0} is invalid.".format(post_id)}), mimetype="application/json", status=404)
        ## Check if the user is authorized (followed by the current user)
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({"message": "You cannot view this post: {0}.".format(post_id)}), mimetype="application/json", status=404)
        ## Check if post_id exists in your bookmark
        bm_query = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        bm_post_ids = [bm.post_id for bm in bm_query]
        if post_id in bm_post_ids:
            return Response(json.dumps({"message": "You already bookmarked post_id={0}.".format(post_id)}), mimetype="application/json", status=400)
        
        user_id = self.current_user.id
        ## Create a new bookmark
        new_bm = Bookmark (user_id, post_id)
        ## add to database
        db.session.add(new_bm)
        db.session.commit()
        # ----------------------------------------------------------------- #
        return Response(json.dumps(new_bm.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        ## TODO: DELETE "bookmark" record where "id"=id
        # print(id)
        bm_query = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        bm_ids = [bm.id for bm in bm_query]
        # print(bm_ids)
        if id in bm_ids:
            Bookmark.query.filter_by(id=id).delete()
            ## commit changes to database
            db.session.commit()
            return Response(json.dumps({"message": "Bookmark id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)
        return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
