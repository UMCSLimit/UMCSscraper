from flask import Flask, Response
from flask_restful import Resource, Api, reqparse, abort
app = Flask(__name__)
from scrape import scrape

sampleList = scrape()

@app.route('/')
def printList():
    return Response(
            response=sampleList,
            status=200,
            mimetype='application/json')
