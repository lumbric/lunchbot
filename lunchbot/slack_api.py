import time
from slackclient import SlackClient
from lunchbot.config import slack_bot_token

# test channel (slackbot)
#CHANNEL = 'UF484D7Q8'

# lunch channel
CHANNEL = 'CFKP93MSN'


def _add_poll_option(sc, timestamp, poll_opt):
    reply = sc.api_call("reactions.add", channel=CHANNEL,
                        timestamp=timestamp, name=poll_opt)
    if not reply['ok']:
        raise RuntimeError(f"Could not post message to slack: {reply['error']}")


def post_menu(menu, poll_options):
    token = slack_bot_token()
    sc = SlackClient(token)

    reply = sc.api_call('chat.postMessage', channel=CHANNEL, text=menu)
    if not reply['ok']:
        raise RuntimeError(f"Could not post message to slack: {reply['error']}")

    timestamp = reply['ts']

    for poll_opt in poll_options:
        time.sleep(2.)  # should help to get poll options ordered
        _add_poll_option(sc, timestamp, poll_opt)
