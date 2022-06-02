import React from 'react';

class Stories extends React.Component {

    // Component 1
    constructor(props) {
        super(props);
        // initialization code here
        console.log('Stories component created');
    }

    // Component 2
    componentDidMount() {
        // fetch posts and then set the state...
        console.log('Stories component mounted');
    }

    // Component 3
    render() {
        return (
            <header className="stories">
                Stories 123
                {/* Stories */}
            </header>
        );
    }
}

export default Stories;