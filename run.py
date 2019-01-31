from flask import Flask
from scrape import scrape
app = Flask(__name__)
 
@app.route("/")
def hello():
	return("TEST")
 
if __name__ == "__main__":
	app.run()