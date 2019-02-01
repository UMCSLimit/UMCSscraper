from flask import Flask, Response
from flask_cors import CORS
from scrape import scrape
#from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
CORS(app)

sampleList = scrape()

@app.route('/')
def printList():
    return Response(
            response=sampleList,
            status=200,
            mimetype='application/json')
