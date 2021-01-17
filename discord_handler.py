import time
import os
import signal
import sys
import threading
import json

import discordsdk as dsdk

from firebase_handler import FirebaseHandler

APP_ID = 799831774959763488
COLOR_MD_KEY = "COLOR_MAPPING"

def dummy_callback(result, *args):
    if result != dsdk.Result.ok:
        raise Exception(result)

class DiscordHandler:
    def __init__(self):
        self.app = dsdk.Discord(APP_ID, dsdk.CreateFlags.default)

        self.lobby_manager = self.app.get_lobby_manager()
        self.voice_manager = self.app.get_voice_manager()
        self.user_manager = self.app.get_user_manager()

        self.lobby_id = None
        self.activity_secret = None
        self.color_mapping = {}

        self.lobby_manager.on_member_connect = self.on_member_connect
        self.lobby_manager.on_member_disconnect = self.on_member_disconnect
        self.user_manager.on_current_user_update = self.on_curr_user_update

        self.firebase = FirebaseHandler()

        signal.signal(signal.SIGINT, self.signal_handler)

    def create_lobby(self):
        transaction = self.lobby_manager.get_lobby_create_transaction()

        transaction.set_capacity(10)
        transaction.set_type(dsdk.enum.LobbyType.public)
        transaction.set_metadata("GAME_ID", "ABCDEF")

        self.lobby_manager.create_lobby(transaction, self.create_lobby_callback)

    def join_lobby(self, activity_secret):
        self.activity_secret = activity_secret
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
            self.lobby_id = lobby.id

            member_count = self.lobby_manager.member_count(lobby.id)

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
            self.lobby_manager.disconnect_lobby(self.lobby_id, dummy_callback)
        else:
            raise Exception(result)

    def adjust_user_volume(self, user_id, volume):
        try:
            if user_id != self.user_id:
                self.voice_manager.set_local_volume(user_id, volume)
                print(f"adjusted volume of {str(user_id)[:-5]} to {volume}")
        except Exception as e:
            print("error adjusting volume", e)

    def on_member_connect(self, lobby_id, user_id):
        if lobby_id == self.lobby_id:
            self.adjust_user_volume(user_id, 0)
            print(f"{user_id} has joined the lobby!")

    def on_member_disconnect(self, lobby_id, user_id):
        if lobby_id == self.lobby_id:
            print(f"{user_id} has left the lobby!")

    def on_curr_user_update(self):
        user = self.user_manager.get_current_user()
        self.user_id = user.id

    def update_color_map(self, color):
        self.firebase.db.child(self.lobby_id).child("colors").update({color: str(self.user_id)})

    def signal_handler(self, signal, frame):
        self.disconnect()
        time.sleep(3)
        sys.exit(0)
        
    def run(self):
        thread = threading.Thread(target=self._spin, daemon=True)
        thread.start()
        
    def _spin(self):
        ticker = 0
        while True:
            time.sleep(1/10)
            self.app.run_callbacks()
            ticker += 1
            if ticker == 10:
                path = self.firebase.db.child(self.lobby_id).child("colors")
                val = path.get().val()
                self.color_mapping = val if val else {}
                ticker = 0


if __name__ == "__main__":
    dh = DiscordHandler()
    dh.create_lobby()
    dh.run()

    time.sleep(2)
    while True:
        time.sleep(1)
        dh.testing()
