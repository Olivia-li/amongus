import time

import discordsdk as dsdk


# we get the application id from a file
with open("application_id.txt", "r") as file:
    application_id = int(file.read())

# we create the discord instance
app = dsdk.Discord(application_id, dsdk.CreateFlags.default)
user_manager = app.get_user_manager()


# events
def on_current_user_update():
    print("[on_current_user_update]")
    user = user_manager.get_current_user()
    print(f"Hello, {user.username}#{user.discriminator}!")

    premium_type = user_manager.get_current_user_premium_type()
    if premium_type == dsdk.PremiumType.none_:
        print("You are not a nitro subscriber.")
    elif premium_type == dsdk.PremiumType.tier_1:
        print("You are a nitro classic subscriber!")
    elif premium_type == dsdk.PremiumType.tier_2:
        print("You are a nitro subscriber!")

    if user_manager.current_user_has_flag(dsdk.UserFlag.hype_squad_house_1):
        print("You are a member of house bravery.")
    if user_manager.current_user_has_flag(dsdk.UserFlag.hype_squad_house_2):
        print("You are a member of house brillance.")
    if user_manager.current_user_has_flag(dsdk.UserFlag.hype_squad_house_3):
        print("You are a member of house balance.")


# bind events
user_manager.on_current_user_update = on_current_user_update


def callback(result, user):
    if result != dsdk.Result.ok:
        print(f"We failed to get user (result {result})")
    else:
        print(f"We have found the owner! {user.username}#{user.discriminator}")


# we search for the owner of the repo
user_manager.get_user(425340416531890178, callback)

while 1:
    time.sleep(1/10)
    app.run_callbacks()
