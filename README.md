# freqbot-dockerized
A template for docker based FreqBot application

How-to run:
```
$ git clone https://github.com/zen-tools/freqbot-dockerized.git
$ cd freqbot-dockerized
~/freqbot-dockerized $ docker build -t freqbot .
~/freqbot-dockerized $ docker run -d -e ACCOUNT="syslog@jabber.ua" -e PASSWD="******" -e NICK="SysLog" -e ADMINS="your-jid@jabber.ua, more-jid@jabber.ua" -v /tmp/data:/data --name jabber-bot freqbot
```

