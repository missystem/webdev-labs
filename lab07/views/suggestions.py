from flask import Response, request
from flask_restful import Resource
from models import User, Following
from views import get_authorized_user_ids
import json
import random

# Credits:
# Remove all the elements that occur in one list from another
# https://stackoverflow.com/questions/4211209/remove-all-the-elements-that-occur-in-one-list-from-another
#


class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # TODO: suggestions should be any user with an ID that's not in this list:
        ## OPTIMIZED VERSION
        ## List of suggested users to follow
        ## use the User data model to get this information
        ## just display 7 users that the current user isn't already following
        # ---------------------- code start here -----------------------
        ## all users that current user is following
        user_ids = get_authorized_user_ids(self.current_user)
        ## query 7 users from all users but exclude user_ids (followings)
        suggestions = User.query.filter(~User.id.in_(user_ids)).limit(7).all()
        suggestions_json = [t.to_dict() for t in suggestions]
        # --------------------------------------------------------------
        return Response(json.dumps(suggestions_json), mimetype="application/json", status=200)
    
def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint,
        '/api/suggestions',
        '/api/suggestions/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
