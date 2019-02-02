from flask import Flask, Response
from flask_cors import CORS
from scrape import scrape
from apscheduler.schedulers.background import BackgroundScheduler
import json
app = Flask(__name__)
CORS(app)


# TO DO
# Parse json here and add success message
# Only change main object if new update
# Dont change main object if it's not working
newsFeed = ''
def checkIfBroken(news):
	item_dict = json.loads(news)
	if len(item_dict) == 8:
		return 0
	else:
		return 1

def updateNewsFeed():
    global newsFeed
    feed = scrape()
    broken = checkIfBroken(feed)
    if broken == 0:
    	newsFeed = feed

@app.route('/')
def printList():
    return Response(
            response=newsFeed,
            status=200,
            mimetype='application/json')

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(updateNewsFeed, 'interval', seconds=15)
scheduler.start()

if __name__ == '__main__':
    app.run()
