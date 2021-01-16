import time
import uuid

import discordsdk as dsdk

# we get the application id from a file
with open("application_id.txt", "r") as file:
    application_id = int(file.read())


# debug callback
def debug_callback(debug, result, *args):
    if result == dsdk.Result.ok:
        print(debug, "success")
    else:
        print(debug, "failure", result, args)


# we create the discord instance
app = dsdk.Discord(application_id, dsdk.CreateFlags.default)
activity_manager = app.get_activity_manager()


# events
def on_activity_join(secret):
    print("[on_activity_join]")
    print("Secret", secret)


def on_activity_spectate(secret):
    print("[on_activity_spectate]")
    print("Secret", secret)


def on_activity_join_request(user):
    print("[on_activity_join_request]")
    print("User", user.Username)

    activity_manager.send_request_reply(
        user.Id,
        dsdk.ActivityJoinRequestReply.yes,
        lambda result: debug_callback("send_request_reply", result)
    )


def on_activity_invite(type, user, activity):
    print("[on_activity_invite]")
    print("Type", type)
    print("User", user.Username)
    print("Activity", activity.State)

    activity_manager.accept_invite(user.Id, lambda result: debug_callback("accept_invite", result))


# bind events
activity_manager.on_activity_join = on_activity_join
activity_manager.on_activity_spectate = on_activity_spectate
activity_manager.on_activity_join_request = on_activity_join_request
activity_manager.on_activity_invite = on_activity_invite

# we create an activity
activity = dsdk.Activity()
activity.state = "Testing Game SDK"
activity.party.id = str(uuid.uuid4())
activity.party.size.current_size = 4
activity.party.size.max_size = 8
activity.secrets.join = str(uuid.uuid4())

# we update the activity
activity_manager.update_activity(activity, lambda result: debug_callback("update_activity", result))

# we set the command
activity_manager.register_command("iexplore.exe http://www.example.com/")

timer = 0

while 1:
    time.sleep(1/10)
    app.run_callbacks()

    timer += 1
    if timer == 600:  # clear activity after 60 seconds
        activity_manager.clear_activity(lambda result: debug_callback("clear_activity", result))
