__author__ = 'FrancisScreene'

import time
import os

from slackclient import SlackClient
import requests


def connect_and_send(channelname, message):
    config = dict()
    with open('api.conf') as conf:
        lines = conf.read()
        for line in lines:
            sp = line.split('=')
            config[sp[0]] = sp[1]

    sc = SlackClient(config['apiToken'])

    for i in range(0, 5):
        if sc.rtm_connect():
            id = str(sc.server.channels.find(channelname)).split("\n")[0].split(" : ")[1]
            sc.rtm_send_message(id, message)
            break
        else:
            print "Connection failed (" + i + "), retrying in 1 second..."
            time.sleep(1)


# connectAndSend("bottestchannel", "<!channel> Test Message Please Ignore, I am just a menial machine")

def get_kills():
    headers = {'User-Agent': 'Adhocracy Killmail Bot, Maintainer: Francis (fscreene@icloud.com', 'accept-encoding': 'gzip'}
    request = requests.get('https://zkillboard.com/api/w-space/corporationID/1267072316/pastSeconds/3600', headers=headers)

def run():

        path = os.getcwd() + "/python/SlackAlertBot/"
        stamps = open(path + "cache.txt")
        for line in stamps:
            st.append(line)
        stamps.close()
        if (timestamp + "\n") not in st:
            connectAndSend("alerts", "<!channel>: " + "\n".join(msg.get_payload(decode=True).split("\n")[0:-3]))
            f = open(path + "cache.txt", 'a')
            f.write(timestamp + "\n")
            f.close()


run()