from flask import Flask, Response
from flask_cors import CORS
from scrape import scrape, Scraper
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# TO DO
# Send last updated notice ?

myScraper = Scraper(timeout=15)

@app.route('/')
def getNews():
	return Response(
		response=myScraper.jsonData,
		status=200,
		mimetype='application/json'
	)

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(myScraper.start, 'interval', seconds=myScraper.timeout)
scheduler.start()

if __name__ == '__main__':
    app.run()
