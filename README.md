![](https://cloud.githubusercontent.com/assets/109988/10342246/2f1fe848-6ce6-11e5-9347-7021c740b1d5.png)

A Python-based SlackBot derived from [SlackHQ's](https://github.com/slackhq/) remarkable [RTMBot](https://github.com/slackhq/python-rtmbot)

## Getting started

* This bot uses MongoDB instead of the filesystem for persistence. You can install MongoDB locally (default) or export `CAMPFINBOT_MONGO_URL` with your custom connection string.
```
brew install mongodb
ln -sfv /usr/local/opt/mongodb/*.plist ~/Library/LaunchAgents
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist
```

* Create a virtualenv and install the required packages.
```
mkvirtualenv nyt-campfinbot && pip install -r requirements.txt
```

* Create a bot integration for your campfinbot and get the [channel ID](https://api.slack.com/methods/channels.list/test). Then export the channel ID and the token.
```
export CAMPFINBOT_SLACK_CHANNEL=C012345
export CAMPFINBOT_SLACK_TOKEN=ABCEFGHIJKLMNOPQRSTUVWXYZ01234567890
```

* Export the hosts for preloaded data.
```
CAMPFINBOT_CANDIDATES_HOST=interactive-api.newsdev.nytimes.com
CAMPFINBOT_FILINGS_HOST=projects.nytimes.com
```

* Create the log file if it doesn't exist.
```
touch /tmp/campfinbot.log
```

* Preload data for the bot. It needs some committees and would appreciate knowing about old filings so it doesn't spam your slack channel with stuff you already know about.
```
python -m campfinbot.preload
```

* Run the bot itself.
```
python -m campfinbot.bot
```

* Tail the log to see what's going on.
```
tail -f /tmp/campfinbot.log
``` 

## Deployment
* Make an upshot script in `/etc/init/campfinbot.conf` and use this template.
```
start on runlevel [2345]
stop on runlevel [!2345]

respawn

script
  export CAMPFINBOT_CANDIDATES_HOST='interactive-api.newsdev.nytimes.com'
  export CAMPFINBOT_SLACK_CHANNEL='C012345'
  export CAMPFINBOT_FILINGS_HOST='projects.nytimes.com'
  export CAMPFINBOT_SLACK_TOKEN='xoxb-1234567890-AbcDefGhijkLmNOpQRstUvWXyz'
  export CAMPFINBOT_PRD_HOST='ec2-0-0-0-0.compute-99.amazonaws.com'
  export CAMPFINBOT_MONGO_URL='127.0.0.1:12345'
  cd /home/ubuntu/nyt-campfinbot && /home/ubuntu/.virtualenvs/nyt-campfinbot/bin/python /home/ubuntu/nyt-campfinbot/campfinbot/bot.py
end script
```