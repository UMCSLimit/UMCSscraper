from flask import Flask, Response
from flask_cors import CORS
from scrape import Scraper
from insta import instaScraper
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# TO DO
# Send last updated notice ?

myScraper = Scraper(timeout=5)
instaScraper = instaScraper()
@app.route('/')
def getNews():
	return Response(
		response=myScraper.jsonData,
		status=200,
		mimetype='application/json'
	)
@app.route('/i')
def getInsta():
	return Response(
		response=instaScraper.jsonData,
		status=200,
		mimetype='application/json'
		)


scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(myScraper.start, 'interval', seconds=myScraper.timeout)
scheduler.add_job(instaScraper.start, 'interval', seconds=60, max_instances = 5)
scheduler.start()

if __name__ == '__main__':
    app.run()
