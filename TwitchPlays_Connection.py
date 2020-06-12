# DougDoug Note: 
# This is the code that connects to twitch and checks for new messages.
# You should not need to modify anything in this file, just use as is.

# Almost all code in this file is from Wituz's "Twitch Plays" tutorial at:
# http://www.wituz.com/make-your-own-twitch-plays-stream.html

# Updated to Python 3 by ClassyWeasel

import socket
import sys
import re

class Twitch:

    user = "";
    oauth = "";
    s = None;

    def twitch_login_status(self, data):
        if not re.match((r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$').encode(), data): return True
        else: return False

    def twitch_connect(self, user, key):
        self.user = user;
        self.oauth= key;
        print("Connecting to twitch.tv");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.settimeout(0.6);
        connect_host = "irc.twitch.tv";
        connect_port = 6667;
        try:
            s.connect((connect_host, connect_port));
        except:
            print("Failed to connect to twitch");
            sys.exit();
        print("Connected to twitch");
        print("Sending our details to twitch...");
        s.send(('USER %s\r\n' % user).encode());
        s.send(('PASS %s\r\n' % key).encode());
        s.send(('NICK %s\r\n' % user).encode());

        if not self.twitch_login_status(s.recv(1024)):
            print("... and they didn't accept our details");
            sys.exit();
        else:
            print("... they accepted our details");
            print("Connected to twitch.tv!")
            self.s = s;
            s.send(('JOIN #%s\r\n' % user).encode())
            s.recv(1024);

    def check_has_message(self, data):
        longString2 = (r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$').encode()
        return re.match(longString2, data)

    def parse_message(self, data):
        return {
            'channel': re.findall((r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :').encode(), data)[0],
            'username': re.findall((r'^:([a-zA-Z0-9_]+)\!').encode(), data)[0],
            'message': re.findall((r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)').encode(), data)[0].decode('utf8')
        }

    def twitch_recieve_messages(self, amount=1024):
        data = None
        try: data = self.s.recv(1024);
        except: return False;

        if not data:
            print("Lost connection to Twitch, attempting to reconnect...");
            self.twitch_connect(self.user, self.oauth);
            return None

        #self.ping(data)

        if self.check_has_message(data):
            return [self.parse_message(line) for line in filter(None, data.split(('\r\n').encode()))];
