import React from 'react';
import Posts from './Posts.js';
import Stories from './Stories.js';
import Suggestions from './Suggestions.js'
import Profile from './Profile.js';
import NavBar from './NavBar.js';
import { getHeaders } from './utils.js';

{/* TODO: Break up the HTML below into a series of React components. */}
class App extends React.Component {  

    constructor(props) {
        super(props);
        // issue a fetch request to /api/profile endpoint:
        this.getProfileFromServer();
        this.state = {
            user: {}
        }
    }

    getProfileFromServer () {
        fetch('/api/profile', {
            headers: getHeaders()
        }).then(response => response.json())
        .then(data => {
            console.log(data);
            this.setState({
                user: data
            })
        })
    }

    render () {
        return (
            <div>
                <NavBar title="Photo App" username={this.state.user.username} />
                <aside>
                    <Profile />
                    <Suggestions />
                </aside>

                <main className="content">
                    <Stories />
                    <Posts />
                </main>
            </div>
        );
    }
}

export default App;