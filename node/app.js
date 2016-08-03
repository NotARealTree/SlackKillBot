var config = require('./config');
var request = require('request');
var slack = require('./slack');

setInterval(function(){
    request('http://redisq.zkillboard.com/listen.php', (err, res, body) => {
        if(body != null){
            var json = JSON.parse(body);
            if(json.package != null){
                var killmail = json.package.killmail;
                if(killmail.solarSystem.id in config.systems){
                    var message = {
                        title: 'Kill in Metro',
                        text: format(killmail) + '\n' + formatMailLink(json) + '\n' + formatSystemLink(killmail)
                    };
                    slack.sendMessage(message);
                }
            }
        }
    });
}, 1000);

function format(killmail){

    var killer = killmail.attackers.filter(function(attacker){
        return attacker.finalBlow;
    })[0];

    var numKillers = killmail.attackers.length;

    var formatted = killmail.solarSystem.name + ': "';

    if('character' in killmail.victim){
        formatted += killmail.victim.character.name;
    }else{
        formatted += killmail.victim.shipType.name;
    }

    formatted += '" - "' +
    killmail.victim.corporation.name + '" was killed by "';

    if('character' in killer){
        formatted += killer.character.name;
    }else{
        formatted += killer.shipType.name;
    }
    formatted += '" - "';

    if('corporation' in killer){
        formatted += killer.corporation.name + '" in a ';
    }

    formatted += killer.shipType.name + '. ' +
    numKillers + ' ship' + (numKillers > 1 ? 's' : '') + ' involved.';
    return formatted;
}

function formatMailLink(json){
    return 'Killmail: https://zkillboard.com/kill/' + json.package.killID + '/';
}

function formatSystemLink(killmail){
    return 'System: http://evemaps.dotlan.net/system/' + killmail.solarSystem.name;
}