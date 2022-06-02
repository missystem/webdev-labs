import React from 'react';

class NavBar extends React.Component {

    // Component 1
    constructor(props) {
        super(props);
        console.log('NavBar props:', props)
        // initialization code here
    }

    // Component 2
    componentDidMount() {
        // fetch posts and then set the state...
        console.log('NavBar component mounted');
    }

    // Component 3
    render() {
        return (
            <nav className="main-nav">
                <h1>{this.props.title}</h1>
                <ul>
                    <li><a href="/api">API Docs</a></li>
                    <li><span>{this.props.username}</span></li>
                    <li><a href="/logout">Sign out</a></li>
                </ul> 
            </nav>
        );
    }
}

export default NavBar;