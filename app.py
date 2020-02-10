from flask import Flask, Response
from flask import request
from flask_cors import CORS
from scrape import Scraper
from insta import InstaScraper
from events import events
from ztm import ZTM
from weather import Weather
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
CORS(app)

# TO DO

umcsScraper = Scraper(timeout=15)
instaScraper = InstaScraper()
instaScraper.start()
ztm = ZTM()
weather = Weather()

@app.route('/news')
def getNews():
	return umcsScraper.response()
@app.route('/events')
def getEvents():
	return events()
@app.route('/instagram')
def getInsta():
	return instaScraper.response()
@app.route('/weather')
def getWx():
	return weather.getwxmain()

@app.route('/ztm')
def get_metadata():
	return Response(
		response=ztm.get_metadata(),
		status=200,
		mimetype='application/json'
	)

@app.route('/ztm/getBuses')
def get_buses():
	return Response(
		response=ztm.buses(req=request.get_json()),
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
scheduler.add_job(umcsScraper.start, 'interval', seconds=1000)
scheduler.add_job(events, 'interval', seconds=1000)
scheduler.add_job(weather.getwxmain, 'interval', seconds=300)
scheduler.add_job(instaScraper.start, 'interval', seconds=1000, max_instances=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3113)
