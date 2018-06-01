#bot config
HOST = "irc.twitch.tv"              # This is Twitchs IRC server
PORT = 6667                         # Twitchs IRC server listens on port 6767
NICK = "bdavsbot"            # Twitch username your using for your bot
PASS = "oauth:hk62g8etd3t44q5trcee9ggztiq4i2" # your Twitch OAuth token
CHAN = "#bdavs77"
#CHAN = "#accidentalgrenade"                   # the channel you want the bot to join.
#CHAN = "#huttsgaming"
#CHAN = "#magnusrayneg4l"
#CHAN = "#chinoxg4l"
RATE = (20/30) # messages per seccond
SEARCH_PAT = [
    r"test"
#    r"swear",
#    r"some_pattern"
]
MOD_COMMAND = r"!setmessage"

#interface config
SPEEDX = 2
SPEEDY = 2
RPI = 0
TIMEOUT = 1000
FONT_SIZE = 22
BG = "green"
FG = "white"
#FG = '#FF0000'
REFRESH = 10
