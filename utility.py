import config
import socket
import re
from collections import namedtuple


Emote = namedtuple('Emote', ('id', 'start', 'end'))
#CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

def parse_emotes(raw):
    emotes = []
    for raw_emote in raw.split('/'):
        id, locations = raw_emote.split(':')
        id = int(id)
        locations = [location.split('-')
                     for location in locations.split(',')]
        for location in locations:
            emote = Emote(id=id, start=int(location[0]), end=int(location[1]))
            emotes.append(emote)
    return emotes
#data = r'@badges=bits/1;color=#008000;display-name=WH1T33Y3BR0WM4N;emotes=;id=dafd7155-fd20-4230-a432-8ad639e63e7d;mod=0;room-id=51194830;subscriber=0;tmi-sent-ts=1526503294681;turbo=0;user-id=157325844;user-type= :wh1t33y3br0wm4n!wh1t33y3br0wm4n@wh1t33y3br0wm4n.tmi.twitch.tv PRIVMSG #accidentalgrenade :burpees fucking suck'
#data = r'@badges=moderator/1;color=#0000FF;display-name=2Cubed;emotes=25:6-10,12-16;id=05aada01-f8c1-4b2e-a5be-2534096057b9;mod=1;room-id=82607708;subscriber=0;turbo=0;user-id=54561464;user-type=mod :2cubed!2cubed@2cubed.tmi.twitch.tv PRIVMSG #innectic :Hiya! Kappa Kappa'

#bits
data = r"@badges=subscriber/3,bits/100000;bits=100;color=#FF69B4;display-name=deezelia;emotes=;id=0dd83684-5d93-4566-bfbc-779e1409fd88;mod=0;room-id=65264217;subscriber=1;tmi-sent-ts=1526516807352;turbo=0;user-id=150353640;user-type= :deezelia!deezelia@deezelia.tmi.twitch.tv PRIVMSG #huttsgaming :cheer100 Happy Birthday Hutts! Sorry i havent been around in a while"

#self sub
data = r"@badges=subscriber/0,premium/1;color=;display-name=deadshot67676;emotes=;id=20f3ceaf-ace8-49e1-868c-8959e066baca;login=deadshot67676;mod=0;msg-id=sub;msg-param-months=1;msg-param-sub-plan-name=Hutts\sGaming\sSubscription;msg-param-sub-plan=Prime;room-id=65264217;subscriber=0;system-msg=deadshot67676\sjust\ssubscribed\swith\sTwitch\sPrime!;tmi-sent-ts=1526517256323;turbo=0;user-id=223438310;user-type= :tmi.twitch.tv USERNOTICE #huttsgaming"

#gift sub
data = r"@badges=sub-gifter/1;color=#FF0000;display-name=RNGsmiles;emotes=;id=73cb1ca3-c0bd-49bc-bc66-eee6e6489cca;login=rngsmiles;mod=0;msg-id=subgift;msg-param-months=1;msg-param-recipient-display-name=Frankthenontank;msg-param-recipient-id=36266484;msg-param-recipient-user-name=frankthenontank;msg-param-sender-count=5;msg-param-sub-plan-name=Hutts\sGaming\sSubscription;msg-param-sub-plan=1000;room-id=65264217;subscriber=0;system-msg=RNGsmiles\sgifted\sa\sTier\s1\ssub\sto\sFrankthenontank!\sThey\shave\sgiven\s5\sGift\sSubs\sin\sthe\schannel!;tmi-sent-ts=1526517040131;turbo=0;user-id=109038977;user-type= :tmi.twitch.tv USERNOTICE #huttsgaming"


def parse_msg(data):
    try:
        meta, user, msgtype, channel, message = data.split(' ', maxsplit=4)
    #print(meta)
        #try:
        meta = dict(tag.split('=') for tag in meta.split(';'))
        user = re.search(r"\w+", user).group(0)
        message = message[1:]
     #   except:
  #  print("dict parse failed")
 #   meta['emotes'] = parse_emotes(meta['emotes'])
        rtn = {'meta':meta, 'user':user, 'msgtype':msgtype, 'channel':channel, 'message':message}
    except:
       print('message parse failed') #data)
       rtn=None
    print(rtn)
    return(rtn)

def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msg)).encode("UTF-8"))

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))

def test(sock, user):
    chat(sock, "{} said something".format(user))
#parse_msg(data)
