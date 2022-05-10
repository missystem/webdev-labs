## Installation

See Lab 2 (<https://cs396-web-dev.github.io/spring2022/assignments/lab02>) for instructions on how to:

1. set up your virtual environment,
2. install the dependencies,
3. set up the Flask environment variables, and
4. run your Flask app

## Navigation
* [HW 1](#HW-1-Instruction)
* [HW 2](#HW-2-Instruction)
* [HW 3](#HW-3-Instruction)

---

## [HW 1 Instruction](https://cs396-web-dev.github.io/spring2022/assignments/hw01)
### Outline
```
<body>
    <nav id="navigation-bar">
    </nav>

    <section id="main">
        <div class="left-panel">
            <div class="stories">
            </div>
            <div class="posts">
            </div>
        </div>

        <div class="right-panel">
        </div>
    </section>
</body>
```

#### [Navigation](#Navigation)

---

## [HW 2 Instruction](https://cs396-web-dev.github.io/spring2022/assignments/hw02)
### Organize files
```
photo-app
├── .git                        # your local git repo (that you created for HW1)
├── Procfile
├── README.md
├── app.py
├── fake_data.py
├── requirements.txt
├── static
│   ├── starter_style.css
│   └── style.css               # your CSS file from HW1
└── templates
    ├── index.html              # your HTML file from HW1
    └── starter_template.html
```

### Set Up Virtual Environment
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt    # install dependencies

# set environment variables (you just have to do this once per session)
export FLASK_APP=app.py     
export FLASK_ENV=development

# then run flask (type Ctrl+C to quit)
flask run
```

### Finished File Tree
```
photo-app
├── Procfile
├── README.md
├── app.py
├── fake_data.py
├── other-files                 # create an other-files folder for your submission
|   ├── writeup.txt             # accessibility write-up
|   ├── GitHub-Screenshot.png   # screenshot of your git repo
│   └── Wave-Screenshot.png     # screenshot of your accessibility report
├── requirements.txt
├── static
|   ├── starter_style.css
│   └── style.css
└── templates
    ├── includes
    │   ├── navbar.html
    │   ├── cards.html
    │   ├── stories.html
    │   └── suggestions.html
    ├── index.html
    └── starter_template.html
```

#### [Navigation](#Navigation)

---

## [HW 3 Instruction](https://cs396-web-dev.github.io/spring2022/assignments/hw03)

### Questions:
1. Cannot connect GitHub with Heroku?  
[How to switch deployment method from GitHub to Heroku Git with all the changes/app code available in a GitHub repo](https://help.heroku.com/CKVOUPSY/how-to-switch-deployment-method-from-github-to-heroku-git-with-all-the-changes-app-code-available-in-a-github-repo)</br>
2. How to create a hosted database?√
3. How to deploy? (Heroku)√
4. How to get limit posts? √ 
    * do we add '/api/posts?limit=<int:id>', '/api/posts?limit=<int:id>/' into initialize_routes? √ 
5. How to pass unauthorized test?
6. Is the way we get 404 correct? (by using query.get())


### What to Turn In:
* 15 points for GET requests
* 20 points for POST/PATCH/DELETE requests
* 5 points for deploying to Heroku
 
* A link to Heroku deployment: 
  * <https://photo-app-s22.herokuapp.com/api>
  * <https://photo-app-s22.herokuapp.com/>
* DB_URL on Heroku Postgres (for automated tests)
  * DB_URL=postgresql://gdwlazslaowivm:59bf67d9a2318cf7e69dcb59041074f51be1de5298fc729740ae5c52ef2fa3f1@ec2-3-209-124-113.compute-1.amazonaws.com:5432/dbvmk72il51lqt
* A zip file of code
* list partner
  * Tianyi Wu, GitHub: ALo0f
* List what extra credit you did as a comment
  * Modify the flask template from HW2 so that it uses data from your database (instead of using the random data from HW2)
  * Create a brand new endpoint that allows the user to like other people’s comments.
  


```
SMART SUGGESTIONS
    """
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # List of suggested users to follow
        # use the User data model to get this information
        # just display 7 users that the current user isn't already following
        
        # ----------- code start here ------------
        following_ids = get_authorized_user_ids(self.current_user)
        print(f"following_ids: {following_ids}")
        all_users = User.query.all()
        all_users_ids = [usr.to_dict().get('id') for usr in all_users]
        
        print(self.current_user.id)
        print(all_users_ids)
        
        sug_list = [x for x in all_users_ids if x not in following_ids]
        print(sug_list)
        
        # display any 7 users that the current user isn't already following
        random7users = random.choices(sug_list, k=7)
        print(f"random 7 users: {random7users}")
        
        suggestions = []
        for i in random7users:
            suggestions.append(User.query.get(i).to_dict())
        print(f"suggestions: {suggestions}")
        # ----------------------------------------
        return Response(json.dumps(suggestions), mimetype="application/json", status=200)
    """

    """
    def get(self):
        ## smart suggestions
        all_followings = get_authorized_user_ids(self.current_user)
        print(all_followings)
        all_followings.remove(self.current_user.id)
        print(all_followings)
        suggestions = set()
        for following in all_followings:
            fosfo = get_authorized_user_ids(User.query.get(following))
            fosfo.remove(following)
            for fo in fosfo:
                suggestions.add(fo)
        suggestions = list(suggestions)
        print(suggestions)
        sug_list = random.choices(suggestions, k=7)
        print(sug_list)
        suggestions_json = [User.query.get(t).to_dict() for t in sug_list]
        return Response(json.dumps(suggestions_json), mimetype="application/json", status=200)
    """

```



#### [Navigation](#Navigation)


--- 


