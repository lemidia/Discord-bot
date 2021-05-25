# This code make a web server on replit.

# For receiving a ping from monitoring server that might be operating somewhere.

# The reason why we make a web server and receve a ping is that
# replit server will go sleep mode if there is no actual situation(typing, ping, etc) on the web server.

# We use this code to keep alive our discord bot.

# Monitoring server that send a ping to a web server refer to following URL.

# https://uptimerobot.com/

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Server is up and running!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
