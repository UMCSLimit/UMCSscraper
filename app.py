from flask import Flask, Response
from flask_cors import CORS
from scrape import Scraper
from insta import instaScraper
from ztm import ZTM
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# TO DO
# Inherit scrape class for feature classes
# If success load is false send status 400
# Make /ztm route work

myScraper = Scraper(timeout=15)
instaScraper = instaScraper()
ztm = ZTM()

@app.route('/news')
def getNews():
	return Response(
		response=myScraper.jsonData,
		status=200,
		mimetype='application/json'
	)

@app.route('/instagram')
def getInsta():
	return Response(
		response=instaScraper.jsonData,
		status=200,
		mimetype='application/json'
		)

@app.route('/ztm')
def get_metadata():
	return Response(
		response=ztm.get_metadata(),
		status=200,
		mimetype='application/json'
	)

@app.route('/ztm/<int:bus_stop_id>')
def get_bus(bus_stop_id):
	return Response(
		response=ztm.requestDeparture(id=bus_stop_id),
		status=200,
		mimetype='application/json'
	)

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(myScraper.start, 'interval', seconds=myScraper.timeout)
scheduler.add_job(instaScraper.start, 'interval', seconds=60, max_instances=5)
scheduler.start()

if __name__ == '__main__':
    app.run()
