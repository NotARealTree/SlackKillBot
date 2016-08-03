var config = require('./config');
var SlackBot = require('slackbots');

var exports = module.exports = {};

var bot = new SlackBot({
    token: config.slack.token,
    name: config.slack.name
});

bot.on('start', function(){});

exports.sendMessage = function(message, color, notify){
    var body = '*' + message.title + '*\n\n' + message.text;
    var params = {
        icon_url    : config.slack.iconUrl,
        as_user     : false,
        attachments : [{
            text        : body,
            color       : color || config.slack.color,
            mrkdwn_in   : [
                'text',
                'pretext'
            ]
        }]
    };
    bot.postMessageToChannel(config.slack.channel, notify ? '<!channel>' : '', params, function(){});
};