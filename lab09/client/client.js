const ws = window.WebSocket || window.MozWebSocket;
// shortcut:
const qs = document.querySelector.bind(document);
let connection;
let username = "";

/********************************************************/
/* 1. Settng up the web socket + socket event listeners */
/********************************************************/
const initializeConnection = ev => {
    const url = qs('#server').value;
    connection = new ws(url);
    console.log(`Connecting to ${url}...`);

    connection.onopen = () => {
        // fires when the server message received indicating an open connection
        console.log("WebSocket connection is open.");
        utils.showLogin();
    };

    connection.onclose = () => {
        // fires when the server message received indicating a closed connection
        console.log("WebSocket connection is closed.");
        alert('Socket server disconnected!');
    };

    connection.onerror = ev => {
        // fires when the server indicates a websocket error
        console.error("WebSocket error observed:", ev);
    };

    // this is what you will be implementing (see below)
    connection.onmessage = handleServerMessage;
};

/********************************************************/
/* 2. Helper functions that send messages to the server */
/********************************************************/
const notify = {
    sendChat: () => {
        if (qs("#message").value !== "") {
            connection.send(JSON.stringify({
                type: "chat",
                text: qs("#message").value,
                username: username
            }));
            qs("#message").value = "";
        }
    },

    triggerFromEnter: (ev, callback) => {
        if (ev.keyCode === 13) {
            ev.preventDefault();
            callback(ev);
        }
    },

    logout: () => {
        if (!connection) {
            return;
        }
        connection.send(JSON.stringify({
            type: "disconnect",
            username: username
        }));
    },

    login: () => {
        username = qs("#name").value;
        if (!username) {
            return;
        }
        if (!connection) {
            return;
        }

        // log into server:
        connection.send(JSON.stringify({
            type: "login",
            username: username
        }));

        // update UI:
        utils.showChatInterface();
    }
}

/************************************************/
/* 3. Event handlers that listen for DOM events */
/************************************************/
qs('#connect').addEventListener('click', initializeConnection);
qs("#set-name").addEventListener("click", notify.login);
qs('#send').addEventListener('click', notify.sendChat);
qs("#server").addEventListener('keyup', ev => {
    notify.triggerFromEnter(ev, initializeConnection);
});
qs("#name").addEventListener('keyup', ev => {
    notify.triggerFromEnter(ev, notify.login);
});
qs("#message").addEventListener('keyup', ev => {
    notify.triggerFromEnter(ev, notify.sendChat);
});

// logout when the user closes the tab:
window.addEventListener('beforeunload', notify.logout);

// load with cursor on the server textbox:
qs("#server").focus();

/******************************************************/
/* 4. Helper Functions that hide and show UI elements */
/******************************************************/
const utils = {
    resetApp: () => {
        connection = null;
        utils.showElements(['#ws-status']);
        utils.hideElements(
            ['#name-display', '#chat-container', '#send-container', '#status']);
        qs("#chat").innerHTML = '';
    },

    showLogin: () => {
        utils.hideElements(['#step1']);
        utils.showElements(['#step2', '#ws-status']);
        qs("#ws-status").textContent = "Connected";
        qs("#name").focus();
    },

    showChatInterface: () => {
        qs("#name-display").textContent = `Signed in as ${username}.`;
        utils.hideElements(['#step2']);
        utils.showElements(
            ['#name-display', '#chat-container', '#send-container', '#status']);
        qs("#message").focus();
    },

    showElements: elements => {
        document.querySelectorAll(elements).forEach(elem => {
            elem.classList.remove('hidden');
        })
    },
    hideElements: elements => {
        document.querySelectorAll(elements).forEach(elem => {
            elem.classList.add('hidden');
        })
    }
};


/********************
 * 5. Your Code Here
 ********************/
const handleServerMessage = ev => {
    const data = JSON.parse(ev.data);
    if (data.type === "login") {
        console.log('A user has just connected:');
        console.log(data);
        const firstLogin = document.querySelectorAll(`#users-list li`).length === 0;
        if (firstLogin) {
            showAllUsers(data);
        } else {
            addUser(data);
        }
    } else if (data.type === "disconnect") {
        console.log('A user has just disconnected:');
        console.log(data);
        removeUser(data);
    } else if (data.type === "chat") {
        console.log('A user has just sent a chat message:');
        console.log(data);
        showChat(data);
    } else {
        console.error("Message type not recognized.");
        console.log(data);
    }
};

// code that responds to messages received from the server:
const showAllUsers = data => {
    // screen reader reads this; invisible to user:
    qs('#users-list').insertAdjacentHTML('afterbegin', '<p class="context">Current Users</p>');

    const template = data.active_users.map(user => {
        return `<li id="${user}">${user}</li>`
    }).join('');
    qs('#users-list ul').innerHTML = template;

    // screen reader reads this for additional context:
    qs('#update').innerHTML = "<p>You have joined the chat</p>";

    // after screen initializes, turn aria live off.
    setTimeout(() => {
        qs('#users-list').setAttribute("aria-live", "off");
    }, 2000);
};

const removeUser = data => {
    const removed = data.user_left;
    qs('#update').innerHTML = `<p>${removed} has left the chat</p>`;
    console.log(removed);
    document.getElementById(removed).remove();
};

const addUser = data => {
    qs('#users-list').setAttribute("aria-live", "off");
    const username = data.user_joined;
    const template = `
            <li id="${username}">${username}</li>
        `;

    if (!document.getElementById('data.user_joined')) {
        qs('#users-list ul').insertAdjacentHTML('beforeend', template);
    }

    // screen reader reads this:
    qs('#update').innerHTML = `<p>${username} has joined the chat</p>`;
};

const showChat = data => {
    if (data.username === username) {
        qs("#chat").insertAdjacentHTML("beforeend", `<div class="right"><strong>You:</strong> <span class="context">say</span> ${data.text}</div>`);
    } else {
        qs("#chat").insertAdjacentHTML("beforeend", `<div class="left"><strong>${data.username}:</strong> <span class="context">says</span> ${data.text}</div>`);
    }
};