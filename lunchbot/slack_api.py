from slackclient import SlackClient

from config import slack_api_token


CHANNEL = 'UF484D7Q8'
#CHANNEL = 'CFKP93MSN'   # lunch channel


def _add_poll_option(sc, timestamp, poll_opt):
    reply = sc.api_call("reactions.add", channel=CHANNEL,
                        timestamp=timestamp, name=poll_opt)
    if not reply['ok']:
        raise RuntimeError(f"Could not post message to slack: {reply['error']}")


def post_menu(menu, poll_options):
    token = slack_api_token()
    sc = SlackClient(token)

    reply = sc.api_call('chat.postMessage', channel=CHANNEL, text=menu)
    if not reply['ok']:
        raise RuntimeError(f"Could not post message to slack: {reply['error']}")

    timestamp = reply['ts']

    for poll_opt in poll_options:
        _add_poll_option(sc, timestamp, poll_opt)
