import time
import os

import discordsdk as dsdk

app = dsdk.Discord(799831774959763488, dsdk.CreateFlags.default)

lobby_manager = app.get_lobby_manager()

transaction = lobby_manager.get_lobby_create_transaction()

transaction.set_capacity(10)
transaction.set_type(dsdk.enum.LobbyType.public)
transaction.set_metadata("a", "123")


def create_lobby_callback(result, lobby):
    if result == dsdk.Result.ok:
        os.environ['LOBBY_ID'] = str(lobby.id)
        os.environ['LOBBY_SECRET'] = lobby.secret
        os.environ['ACTIVITY_SECRET'] = lobby_manager.get_lobby_activity_secret(lobby.id)

        print(f"lobby {lobby.id} created with secret {lobby.secret}")

        transaction = lobby_manager.get_lobby_update_transaction(lobby.id)
        transaction.set_capacity(9)

        lobby_manager.update_lobby(lobby.id, transaction, update_lobby_callback)
    else:
        raise Exception(result)


def update_lobby_callback(result):
    if result == dsdk.Result.ok:
        print(f"lobby {os.environ['LOBBY_ID']} updated")
        print(os.environ['LOBBY_ID'])
        print(os.environ['ACTIVITY_SECRET'])
        print(1)
        lobby_manager.connect_voice(int(os.environ['LOBBY_ID']), connect_voice_callback)
        print(2)
        # lobby_manager.connect_lobby(int(), os.environ['ACTIVITY_SECRET'], connect_lobby_callback)
    else:
        raise Exception(result)

def connect_voice_callback(result):
    if result == dsdk.Result.ok:
        print(f"connected to voice!")
    else:
        raise Exception(result)

def connect_lobby_callback(result, lobby):
    print(lobby)
    if result == dsdk.Result.ok:
        print(f"connected to lobby {os.environ['LOBBY_ID']}")
    else:
        raise Exception(result)

lobby_manager.create_lobby(transaction, create_lobby_callback)

def on_speak(lobby_id, user_id, speaking):
    print(speaking)

lobby_manager.on_speaking = on_speak

while 1:
    time.sleep(1/10)
    app.run_callbacks()