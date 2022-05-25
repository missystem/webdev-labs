'''
To test: python3 -m websockets ws://localhost:8081/
Then paste one of the following messages:
    * { "type": "login", "username": "walter" }
    * { "type": "disconnect" }
    * { "type": "chat", "text": "Hello world!", "username": "walter" }
    
'''

from dotenv import load_dotenv
load_dotenv()

import asyncio
import websockets
import json
import os

logged_in_users = dict()

PORT = os.environ.get('PORT') or os.environ.get('WS_PORT') or 8081

async def respond_to_message(websocket, message):
    try:
        data = json.loads(message)
    except:
        data = { 
            'error': 'error decoding {0}'.format(message),
            'details': 'See instructions for list of valid message formats.'}
        return await websocket.send(json.dumps(data))
    
    
    ## Login
    if data.get('type') == 'login':
        print('LOGIN', data)
        # add user to logged_in_users dict
        logged_in_users[websocket] = data.get('username')
        message = {
            "type": "login",
            "active_users": list(logged_in_users.values()),
            "user_joined": data.get("username")
        }    
    ## Disconnect
    elif data.get('type') == 'disconnect':
        print('DISCONNECT', data)
        user_who_left = logged_in_users[websocket]
        del logged_in_users[websocket]
        message = {
            "type": "disconnect",
            "active_users": list(logged_in_users.values()),
            "user_left": user_who_left
        }
    ## Chat
    elif data.get('type') == 'chat':
        print('CHAT', data)
        message = data
    ## Unrecognized
    else:
        message = {
            'message': 'Unrecognized message type',
            'source': data
        }
        
    # await websocket.send(json.dumps(data))
    for sock in logged_in_users:
        # TODO: replace "data" with a message that conforms to
        # the specs above:
        await sock.send(json.dumps(message))
        
        
    '''
    ******************************************************************
    * Server-Side Logic: Your Job 
    *******************************************************************
    The websocket.send(json.dumps(data)) (line 74, below) 
    echos a received message back to the sender. 
    Your job is to do a little processing and validation of the 
    messages in order to:
        * Track current users / websocket connections.
        * Relay the correct messages to all of the websockets that
          are connected to the server.
           
    Specifically:
    
    1. If the data.get('type') is 'login', add the logged in user to
       the logged_in_users dictionary. Then, send the following message
       back to the clients:
           {
               "type": "login",
               "active_users": list(logged_in_users.values()),
               "user_joined": data.get("username")
           }
       HINT:  Use the following code to REMOVE a tracked user/socket 
       from the server's memory:
            logged_in_users[websocket] = data.get('username')
    
    2. If the data.type is "disconnect", remove the user from
       the logged_in_users dictionary. Then, send the following message
       back to the clients:
           {
               "type": "disconnect",
               "active_users": list(logged_in_users.values()),
               "user_left": data.get("username")
           }
       
       HINT:  Use the following code to REMOVE a tracked user/socket 
       from the server's memory:
            del logged_in_users[websocket]
    
    
    3. If the data.type is "chat", just pass on the entire
       data object to the clients (no processing needed).
    
    4. Otherwise, ignore the message (don't pass it on), and
       log it to the console:
    
            console.log('Unrecognized message type:', data);

    To send messages to all of the clients, iterate through the 
    logged_in_users (which stores each websocket-username) pair.
    ********************************************************************/
    '''


async def broadcast_messages(websocket, path):
    try:
        async for message in websocket:
            await respond_to_message(websocket, message)
    except websockets.ConnectionClosed as e:
        print('A client just disconnected')
        print(e)
    finally:
        if logged_in_users.get(websocket):
            del logged_in_users[websocket]
    

async def main():
    async with websockets.serve(broadcast_messages, "", PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print('Starting web socket server...')
    print('ws://localhost:{0}'.format(PORT))
    asyncio.run(main())