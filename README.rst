lunchbot
========

.. image:: https://travis-ci.org/lumbric/lunchbot.png
   :target: https://travis-ci.org/lumbric/lunchbot
   :alt: Latest Travis CI build status

Provide lunch menu information and vote for options via slack integration.

Note that this is mostly a toy project to test all the tooling required for a
Python project. So don't feel tempted to question the usefulness of the code :)

Installation
------------

.. sourcecode:: bash

    git clone https://github.com/lumbric/lunchbot.git
    cd lunchbot
    virtualenv -p python3 env && source env/bin/activate  # optional
    pip3 install -r requirements.txt
    python3 setup.py install

Configuration
^^^^^^^^^^^^^

Add a Slack API token for your bot to `secrets.yml <config/secrets.yml>`_:

.. sourcecode:: yml

    slack_api_token: 'xoxb-...'

Note that this should be a `bot user token <https://api.slack.com/docs/token-types#bot>`_,
starting with `xoxb-`, otherwise the reactions will be added using your Slack
user and you won't be able to vote using reactions.

Follow the `Slack instructions <https://api.slack.com/bot-users#creating-bot-user>`_
to create the bot user.

Docker
^^^^^^

.. sourcecode:: bash

    cd lunchbot
    docker build -t lunchbot .
    docker run -d --name lunchbot lunchbot

Tests
^^^^^

After cloning GIT repository run:

.. sourcecode:: bash

    tox

Tox will create its own venv environment.

Usage
-----

Run the command

.. sourcecode:: bash

    lunchbot

...to post the daily Mensa menu to your slack channel. There are no additional
options yet. The bot will add each poll option as reaction, so other users can
easily click and add one vote.

Authors
-------

`lunchbot` was written by `lumbric <lumbric@gmail.com>`_.
