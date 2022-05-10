from flask import Response, request
from flask_restful import Resource
from models import Following, User, db, Post, following
import json
from views import get_authorized_user_ids, can_view_post

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # TODO: return all of the "following" records that the current user is following
        # ## Query followings from database
        # followings = Following.query\
        #     .filter(Following.user_id == self.current_user.id)\
        #     .order_by(Following.following_id)\
        #     .all()
        # ## Add followings to a list
        # following_list = []
        # for f in followings:
        #     if f.follower.id == self.current_user.id:
        #         following_list.append(f.to_dict_following())
                
        followings = Following.query.filter_by(user_id = self.current_user.id)
        following_list = [f.to_dict_following() for f in followings]
        ## get info from following
        return Response(json.dumps(following_list), mimetype="application/json", status=200)
        
        
    def post(self):
        # TODO: create a new "following" record based on the data posted in the body 
        body = request.get_json()
        
        ## Check if user_id is provided:
        if not body.get('user_id'):
            return Response(json.dumps({"message": "'user_id' is required."}), mimetype="application/json", status=400)
        
        user_ids = get_authorized_user_ids(self.current_user)
        ## if user_id is not int -> invalid:
        try:
            new_fo_id = int(body.get('user_id'))
        except:
            return Response(json.dumps({"message": "Given id is invalid."}), mimetype="application/json", status=400)
        
        ## if the id is not an existing user:
        if not User.query.get(new_fo_id):
            return Response(json.dumps({"message": "{0} is invalid.".format(new_fo_id)}), mimetype="application/json", status=404)

        ## if user_id is already being followed:
        if new_fo_id in user_ids:
            return Response(json.dumps({"message": "You already followed user: {0}.".format(new_fo_id)}), mimetype="application/json", status=400)
        
        new_following = Following (
            user_id=self.current_user.id,
            following_id=new_fo_id
        )
        db.session.add(new_following)
        db.session.commit()
        # print(new_following)
        return Response(json.dumps(new_following.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # TODO: delete "following" record where "id"=id
        # print(id)
        
        # if user_id is not int -> invalid:
        try:
            id = int(id)
        except:
            return Response(json.dumps({"message": "given id is invalid"}), mimetype="application/json", status=400)
        
        following = Following.query.get(id)
        ## check if the following exists
        if not following:
            return Response(json.dumps({"message": "You did not follow the user: {0}.".format(id)}), mimetype="application/json", status=404)
        ## it's != the curr user -> cannot follow yourself
        if following.user_id != self.current_user.id:
            return Response(json.dumps({"message": "You cannot follow yourself."}), mimetype="application/json", status=404)
        ## delete the following that id=id
        Following.query.filter_by(id=id).delete()
        ## commit the change to the database (to persist the changes)
        db.session.commit()

        return Response(json.dumps({"message": "You have successfully unfollowed {0}.".format(id)}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
