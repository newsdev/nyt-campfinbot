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

* Run the bot itself.
```
python -m campfinbot.bot
```

* Tail the log to see what's going on.
```
tail -f /tmp/campfinbot.log
``` 

* To kill the bot, kill its process (should fix this).
```
ps aux | grep bot

jbowers         47764   1.1  0.3  2518012  45180   ??  S     9:17AM   0:03.95 python -m campfinbot.bot
jbowers         47938   0.0  0.0  2432772    648 s006  S+    9:21AM   0:00.00 grep bot
jbowers         47760   0.0  0.0  2432760    540 s007  S+    9:17AM   0:00.01 tail -f campfinbot.log

kill -9 47764
```