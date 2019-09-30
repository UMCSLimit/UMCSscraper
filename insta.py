from flask import Response
import json
import requests
from instaloader import Instaloader, Profile
from helpers import default_json_response

# TO DO:
# 1. Add async job schedule in app.py // modify it
# 2. Add security in case when the data hasn't been succesfully donwloaded
# 3. Randomize photo selection
# 4. Check what happends with videos

class InstaScraper:
	def __init__(self):
		self.gotInitData = False
		self.jsonData = json.dumps(default_json_response)
		self.loaded = False
		self.posts = []

	def response(self):
		if self.gotInitData:
			return Response(
				response=self.jsonData,
				status=200,
				mimetype='application/json'
			)
		else:
			return Response(
				response=self.jsonData,
				status=400,
				mimetype='application/json'
			)

	def start(self):
		data = self.getInstagramData()
		self.gotInitData = True
		self.jsonData = json.dumps(data)

	def getInstagramData(self):
		self.posts.clear()
		if not self.loaded:
			instaLoader = Instaloader()
			PROFILENAME = 'umcs_lublin'
			profile = Profile.from_username(instaLoader.context, PROFILENAME)
		iter = 0
		for post in profile.get_posts():
			iter += 1
			self.posts.append({
				'photo_url': post.url,
				'caption': post.caption,
				'likes': post.likes
	        })
			if iter == 5:
				break
		request = {
			'success': True,
			'info': {
				'followers': profile.followers
			},
			'payload': self.posts
		}
		return request

if __name__ == "__main__":
	insta = InstaScraper()
	data = json.load(insta.getInstagramData())