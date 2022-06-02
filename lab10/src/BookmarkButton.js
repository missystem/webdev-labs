import React from 'react';
import { getHeaders } from './utils';

class BookmarkButton extends React.Component {

    constructor(props) {
        super(props);
        this.toggleBookmark = this.toggleBookmark.bind(this);
        this.bookmark = this.bookmark.bind(this);
        this.unbookmark = this.unbookmark.bind(this);
        this.requeryPost = this.props.requeryPost.bind(this);
    }

    toggleBookmark(ev) {
        if (this.props.bookmarkId) {
            console.log('unbookmark');
            this.unbookmark();
        } else {
            console.log('bookmark');
            this.bookmark();
        }
    }

    bookmark() {
        fetch('/api/bookmarks', {
            headers: getHeaders(),
            method: 'POST',
            body: JSON.stringify({ post_id: this.props.postId })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.requeryPost();
            })
    }

    unbookmark() {
        fetch(`/api/bookmarks/${this.props.bookmarkId}`, {
            headers: getHeaders(),
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.requeryPost();
            })
    }

    render() {
        const bookmarkId = this.props.bookmarkId;
        return (
            <button role="switch"
                className="bookmark"
                aria-label="Bookmark Button"
                aria-checked={bookmarkId ? 'true' : 'false'}
                onClick={this.toggleBookmark}>
                <i className={bookmarkId ? 'fas fa-bookmark' : 'far fa-bookmark'}></i>
            </button>
        )
    }
}

export default BookmarkButton;