import time

import discordsdk as dsdk
from PIL import Image


# we get the application id from a file
with open("application_id.txt", "r") as file:
    application_id = int(file.read())

# we create the discord instance
app = dsdk.Discord(application_id,  dsdk.CreateFlags.default)
user_manager = app.get_user_manager()
image_manager = app.get_image_manager()


# callbacks
def on_image_loaded(result, handle):
    if result != dsdk.Result.ok:
        print(f"Failed to fetch the image (result {result})")
    else:
        print("Fetched the image!")
        print("Handle:", handle.type, handle.id, handle.size)

        dimensions = image_manager.get_dimensions(handle)
        print("Dimensions:", dimensions.width, dimensions.height)

        # we load the image
        data = image_manager.get_data(handle)
        im = Image.frombytes("RGBA", (dimensions.width, dimensions.height), data)
        im.show()


# events
def on_current_user_update():
    user = user_manager.get_current_user()
    print(f"Hello, {user.username}#{user.discriminator}!")

    # we create an handle
    handle = dsdk.ImageHandle()
    handle.type = dsdk.ImageType.user
    handle.id = user.id
    handle.size = 256

    # we fetch the image
    image_manager.fetch(handle, True, on_image_loaded)


# bind events
user_manager.on_current_user_update = on_current_user_update

while 1:
    time.sleep(1/10)
    app.run_callbacks()
