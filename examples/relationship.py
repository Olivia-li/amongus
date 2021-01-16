import random
import time

import discordsdk as dsdk


# we get the application id from a file
with open("application_id.txt", "r") as file:
    application_id = int(file.read())

# we create the discord instance
app = dsdk.Discord(application_id,  dsdk.CreateFlags.default)
relationship_manager = app.get_relationship_manager()


# events
def on_refresh():
    print("[on_refresh]")

    # we filter friends
    relationship_manager.filter(
        lambda relationship: relationship.type == dsdk.RelationshipType.friend
    )

    # we get how many friends we have!!
    friend_count = relationship_manager.count()
    friends = []
    print(f"You have {friend_count} friends!")

    for n in range(friend_count):
        # we get the friend at index n
        friend = relationship_manager.get_at(n)

        # we add it to the list
        friends.append(friend)

        # we show it
        print(f"{friend.user.username}#{friend.user.discriminator}")

    if len(friends):
        print()

        # we get the friend with a random friend, by his ID
        random_friend = random.choice(friends)
        print(f"Fetching {random_friend.user.id}")

        friend = relationship_manager.get(random_friend.user.id)
        print(f"We found {friend.user.username}.")

    # let's get implicit relationships
    relationship_manager.filter(
        lambda relationship: relationship.type == dsdk.RelationshipType.implicit
    )

    print()
    print("Implicit relationships:")
    for n in range(relationship_manager.count()):
        relationship = relationship_manager.get_at(n)
        print(f"  {relationship.user.username}#{relationship.user.discriminator}")


def on_relationship_update(relationship):
    print("[on_relationship_update]")
    print(f"Relationship {relationship.user.username}")


# bind events
relationship_manager.on_refresh = on_refresh
relationship_manager.on_relationship_update = on_relationship_update

while 1:
    time.sleep(1/10)
    app.run_callbacks()
