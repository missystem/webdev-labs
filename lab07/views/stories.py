from flask import Response
from flask_restful import Resource
from models import Story
from views import get_authorized_user_ids
import json

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # TODO: get stories created by one of these users:
        ## List of stories of users you're following as well as your own story 
        ## (if you have one).  Please use the Story data model to get this information
        ## print(get_authorized_user_ids(self.current_user))
        
        # ---------------------- code start here -----------------------
        ## all the followings
        user_ids = get_authorized_user_ids(self.current_user)
        ## query from Story data model exclude user_ids
        stories = Story.query.filter(Story.user_id.in_(user_ids)).all()
        stories_json = [s.to_dict() for s in stories]
        # print(stories_json)
        # --------------------------------------------------------------
        return Response(json.dumps(stories_json), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
