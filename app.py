from flask import Flask, Response
from flask_cors import CORS
from scrape import Scraper
from insta import InstaScraper
from ztm import ZTM
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
CORS(app)

# TO DO

umcsScraper = Scraper(timeout=15)
instaScraper = InstaScraper()
instaScraper.start()
ztm = ZTM()

@app.route('/news')
def getNews():
	return umcsScraper.response()

@app.route('/instagram')
def getInsta():
	return instaScraper.response()

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
scheduler.add_job(umcsScraper.start, 'interval', seconds=1000)
scheduler.add_job(instaScraper.start, 'interval', seconds=1000, max_instances=5)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3001)