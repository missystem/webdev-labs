import React from 'react';

class Suggestions extends React.Component {

    // Component 1
    constructor(props) {
        super(props);
        // initialization code here
        console.log('Suggestions component created');
    }

    // Component 2
    componentDidMount() {
        // fetch posts and then set the state...
        console.log('Suggestions component mounted');
    }

    // Component 3
    render() {
        return (
            <div className="suggestions">
                <p className="suggestion-text">Suggestions for you</p>
                <div>
                    Suggestions...
                    {/* Suggestions */}
                </div>
            </div>
        );
    }
}

export default Suggestions;