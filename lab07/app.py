from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask import render_template
import os
import json
from sqlalchemy import and_
from models import db, Post, User, Following, ApiNavigator, Story
from views import initialize_routes, get_authorized_user_ids
from tests import utils
import requests
root_url = utils.root_url

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    


db.init_app(app)
api = Api(app)

# set logged in user
with app.app_context():
    app.current_user = User.query.filter_by(id=12).one()


# Initialize routes for all of your API endpoints:
initialize_routes(api)

# Server-side template for the homepage:

@app.route('/')
def home():
    # from hw2 - extra credit 1
    current_user = app.current_user
    user_ids = get_authorized_user_ids(current_user)
    return render_template(
        'index.html', 
        user=current_user,
        posts=Post.query.limit(8).all(),
        stories=Story.query.limit(6).all(),
        # how to get suggestions?
        suggestions=User.query.filter(~User.id.in_(user_ids)).limit(7).all()

    )


@app.route('/api')
def api_docs():
    navigator = ApiNavigator(app.current_user)
    return render_template(
        'api/api_docs.html', 
        user=app.current_user,
        endpoints=navigator.get_endpoints(),
        url_root=request.url_root[0:-1] # trim trailing slash
    )
'''
# from hw2
@app.route('/api/feed')
def get_feed():
    data = requests.get('http://127.0.0.1:5000/posts?=10')
    return json.dumps(data)

@app.route('/api/stories')
def get_stories():
    data = requests.get('http://127.0.0.1:5000/stories?=5')
    return json.dumps(data)

@app.route('/api/suggestions')
def get_suggestions():
    data = requests.get('http://127.0.0.1:5000/suggestions?=8')
    return json.dumps(data)
'''



# enables flask app to run using "python3 app.py"
if __name__ == '__main__':
    app.run()
