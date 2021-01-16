# You need two discord instances running
# This is probably more a test than an example

import os
import time

import discordsdk as dsdk


# We get the Application Id
with open("application_id.txt", "r") as file:
    application_id = int(file.read())


class Game:
    network_manager: dsdk.NetworkManager
    route: dsdk.NetworkManager = None
    instance_id: int
    peer_id: int
    connected: bool = False

    def __init__(self, instance_id):
        self.instance_id = instance_id
        os.environ["DISCORD_INSTANCE_ID"] = str(self.instance_id)

        self.discord = dsdk.Discord(application_id, dsdk.CreateFlags.default)

        self.network_manager = self.discord.get_network_manager()
        self.network_manager.on_route_update = self.on_route_update
        self.network_manager.on_message = self.on_message

        self.peer_id = self.network_manager.get_peer_id()

    def on_route_update(self, route):
        self.route = route
        print(route)
        print(f"[Discord {self.instance_id}] Route: {self.route}")

        self.on_route()

    def on_message(self, peer_id, channel_id, data):
        print(f"[Discord {self.instance_id}] Received from {peer_id} on channel {channel_id}: {repr(data)}")  # noqa: E501


game0 = Game(0)
game1 = Game(1)


def on_game0_route():
    if not game1.connected:
        print(f"[Discord {game1.instance_id}] Connecting to other peer {game0.peer_id} on route {game0.route}")  # noqa: E501
        game1.network_manager.open_peer(game0.peer_id, game0.route)
        game1.network_manager.open_channel(game0.peer_id, 0, True)  # reliable channel
        game1.network_manager.open_channel(game0.peer_id, 1, False)  # unreliable channel
        game1.connected = True
    else:
        game1.network_manager.update_peer(game1.peer_id, game1.route)


def on_game1_route():
    if not game0.connected:
        print(f"[Discord {game0.instance_id}] Connecting to other peer {game1.peer_id} on route {game1.route}")  # noqa: E501
        game0.network_manager.open_peer(game1.peer_id, game1.route)
        game0.network_manager.open_channel(game1.peer_id, 0, True)  # reliable channel
        game0.network_manager.open_channel(game1.peer_id, 1, False)  # unreliable channel
        game0.connected = True
    else:
        game0.network_manager.update_peer(game0.peer_id, game0.route)


game0.on_route = on_game0_route
game1.on_route = on_game1_route

count = 0
next_packet = 0

while 1:
    time.sleep(1/30)
    game0.discord.run_callbacks()
    game1.discord.run_callbacks()

    game0.network_manager.flush()
    game1.network_manager.flush()

    if game0.connected and game1.connected and time.time() > next_packet:
        if count == 30:
            print(f"[Discord {game1.instance_id}] Closing connection to peer {game0.peer_id}.")
            game1.network_manager.close_peer(game0.peer_id)

        # We stop after 40 (*2) sent packets.
        if count == 40:
            break

        else:
            game0.network_manager.send_message(
                game1.peer_id, 0,
                (f"Reliable {count}").encode("ascii")
            )
            print(f"[Discord {game0.instance_id}] Sent a packet to {game1.peer_id} on channel 0.")
            game0.network_manager.send_message(
                game1.peer_id, 1,
                (f"Not reliable {count}").encode("ascii")
            )
            print(f"[Discord {game0.instance_id}] Sent a packet to {game1.peer_id} on channel 1.")
            count += 1

            next_packet = time.time() + 0.5
