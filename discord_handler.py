import time
import os
import signal
import sys
import threading

import discordsdk as dsdk

APP_ID = 799831774959763488

        
class DiscordHandler:
    def __init__(self):
        self.app = dsdk.Discord(APP_ID, dsdk.CreateFlags.default)

        self.lobby_manager = self.app.get_lobby_manager()
        self.voice_manager = self.app.get_voice_manager()

        self.lobby_id = None
        self.activity_secret = None
        self.user_mapping = {}

        self.lobby_manager.on_speaking = self.on_speak
        self.lobby_manager.on_member_connect = self.on_member_connect
        self.lobby_manager.on_member_disconnect = self.on_member_disconnect

        signal.signal(signal.SIGINT, self.signal_handler)

    def create_lobby(self):
        transaction = self.lobby_manager.get_lobby_create_transaction()

        transaction.set_capacity(10)
        transaction.set_type(dsdk.enum.LobbyType.public)
        transaction.set_metadata("a", "123")

        self.lobby_manager.create_lobby(transaction, self.create_lobby_callback)

    def join_lobby(self, activity_secret):
        self.lobby_id, self.activity_secret = activity_secret.split(":")[0], activity_secret
        self.lobby_manager.connect_lobby_with_activity_secret(activity_secret, self.connect_lobby_callback)

    def disconnect(self):
        self.lobby_manager.disconnect_voice(self.lobby_id, self.disconnect_voice_callback)

    def create_lobby_callback(self, result, lobby):
        if result == dsdk.Result.ok:
            self.lobby_id = lobby.id
            self.activity_secret = self.lobby_manager.get_lobby_activity_secret(lobby.id)

            print(f"created lobby {lobby.id} with secret {self.activity_secret}")

            self.lobby_manager.connect_voice(self.lobby_id, self.connect_voice_callback)
        else:
            raise Exception(result)

    def connect_lobby_callback(self, result, lobby):
        if result == dsdk.Result.ok:
            print(f"connected to lobby {lobby.id}")

            self.lobby_manager.connect_voice(lobby.id, self.connect_voice_callback)
        else:
            raise Exception(result)

    def connect_voice_callback(self, result):
        if result == dsdk.Result.ok:
            print(f"connected to voice!")
        else:
            raise Exception(result)

    def disconnect_voice_callback(self, result):
        if result == dsdk.Result.ok:
            self.lobby_manager.disconnect_lobby(self.lobby_id, self.disconnect_lobby_callback)
        else:
            raise Exception(result)

    def disconnect_lobby_callback(self, result):
        if result != dsdk.Result.ok:
            raise Exception(result)

    def adjust_user_volume(self, username, volume):
        if username != self.app.get_user_manager().get_current_user().username:
            user_id = self.user_mapping[username]
            self.voice_manager.set_local_volume(user_id, int(volume * 100))
            print(f"adjusted volume of {username} to {volume}")

    def on_speak(self, lobby_id, user_id, speaking):
        print(lobby_id, user_id, speaking)

    def on_member_connect(self, lobby_id, user_id):
        username = self.lobby_manager.get_member_user(self.lobby_id, user_id).username
        self.user_mapping[username] = user_id

        self.adjust_user_volume(username, 0)
        print(f"{username} has joined the lobby!")

    def on_member_disconnect(self, lobby_id, user_id):
        user = self.lobby_manager.get_member_user(self.lobby_id, user_id)
        username = None
        for uname, _id in self.user_mapping.items():
            if user_id == _id:
                username = self.user_mapping.pop(uname)
                break

        print(f"{username} has left the lobby!")

    def signal_handler(self, signal, frame):
        self.disconnect()
        time.sleep(3)
        sys.exit(0)
        
    def run(self):
        thread = threading.Thread(target=self._spin, daemon=True)
        thread.start()
        
    def _spin(self):
        while True:
            time.sleep(1/10)
            self.app.run_callbacks()

if __name__ == "__main__":
    dh = DiscordHandler()
    dh.create_lobby()
    dh.run()

    while True:
        time.sleep(5)
