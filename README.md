# Among Us Voice Chat and Spectator View

### Setup
In the root folder, do the following:
```
brew install tesseract
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
mkdir lib
```
- install the [discord game sdk](https://dl-game-sdk.discordapp.net/2.5.6/discord_game_sdk.zip) and plop the proper dll (or dlyib) into the newly created lib folder; it may be necessary to remove the extension
- run `python3 main.py`!

### Troubleshooting
If you get `Please make sure to have your Quicktime Movie iPhone Recording open` as an error make sure to enable screen recording for both your IDE and your Terminal. 

