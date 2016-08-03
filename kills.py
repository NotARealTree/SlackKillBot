__author__ = 'Francis Screene'

import time
import os
import json

from slackclient import SlackClient
import requests


def run():
    config = load_config()
    sc = SlackClient(config['api_token'])
    threshold = config['threshold']
    duration = config['duration']
    exclude = config['exclude'].split(';')
    channel_name = config['channel_name']
    corp_name = config['corp_name']
    corp_id = config['corp_id']
    modifiers = config['modifiers']
    user_agent = config['user_agent']

    ids = load_ids()

    kills = get_kills(threshold, duration, exclude, corp_id, modifiers, user_agent, ids)
    if len(kills) > 0:
        message = assemble_message(kills, corp_name)

        for i in range(0, 5):
            if sc.rtm_connect():
                id = str(sc.server.channels.find(channel_name)).split("\n")[0].split(" : ")[1]
                sc.rtm_send_message(id, message)
                break
            else:
                print "Connection failed (" + i + "), retrying in 1 second..."
                time.sleep(1)
    save_ids(ids)


def load_config():
    config = dict()
    with open('api.conf') as conf:
        lines = conf.read().split('\n')
        for line in lines:
            sp = line.split('=')
            if len(sp) > 1:
                config[sp[0]] = sp[1]
    return config


def load_ids():
    with open('ids.json') as jsonfile:
        contents = jsonfile.read()
        jsonfile.close()
    return json.loads(contents)


def save_ids(ids):
    with open('ids.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(ids))
        jsonfile.close()




def get_kills(threshold, duration, exclude, corp_id, modifiers, user_agent, ids):
    cache = cache_ids()
    headers = {'User-Agent': 'Killmail Bot, Maintainer: ' + user_agent,
               'accept-encoding': 'gzip'}
    request_url = ('https://zkillboard.com/api/corporationID/%s/pastSeconds/%s/kills/' + modifiers) % (
    corp_id, duration)
    request = requests.get(request_url, headers=headers)
    jsonkills = request.json()
    newkills = filter((lambda m: m['killID'] not in ids), jsonkills)
    worthkills = filter((lambda m: m['zkb']['totalValue'] > float(threshold)), newkills)

    kills = []

    for kill in worthkills:
        ids.append(kill['killID'])
        # Get killer and number of other involved people
        killer = ''
        involved = 0
        for attacker in kill['attackers']:
            if attacker['finalBlow']:
                killer = str(attacker['characterName'])
            else:
                involved += 1

        # Get link
        link = 'https://zkillboard.com/kill/%d/' % kill['killID']

        # Get worth
        worth = value_to_readable(kill['zkb']['totalValue'])

        # Get Corporation
        corp = str(kill['victim']['corporationName'])

        # get ship
        ship = cache[str(kill['victim']['shipTypeID'])]

        is_not_excluded = True

        for ex in exclude:
            if ex in ship:
                is_not_excluded = False
                break

        if is_not_excluded:
            kills.append((killer, ship, corp, worth, involved, link))

    return kills


def value_to_readable(value):
    value = str(value).split('.')[0]
    if len(value) < 10:
        return value[:-6] + 'M'
    else:
        dec = value[-9:-7]
        bill = value[:-9]
        return '%s.%sB' % (bill, dec)


def assemble_message(kills, corp_name):
    message = '%s killed stuff, specifically, ' % corp_name
    count = 0
    for kill in kills:
        message += '%s killed a %s belonging to %s worth %s ISK with %s other people (%s)' % kill
        if count < len(kills) - 2:
            message += ', '
        else:
            message += ' and '
        count += 1
    message = message[:-5] + '.'
    return message


def cache_ids():
    f = open('ids')
    lines = f.read().split('\r')
    cache = dict()
    for line in lines:
        curr = line.split('\t')
        if len(curr) > 2:
            cache[curr[0]] = curr[2]
    return cache

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run()
