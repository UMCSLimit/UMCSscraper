import json
import requests
from instaloader import Instaloader, Profile
# TO DO:
# 1. Add async job schedule in app.py // modify it
# 2. Add security in case when the data hasn't been succesfully donwloaded
# 3. Randomize photo selection
# 4. Check what happends with videos
class instaScraper:
	def __init__(self):
		self.jsonData = ''

	def start(self):
		data = {
			'success': True,
			'payload': self.getInstagramData()
			}
		self.jsonData = json.dumps(data)

	def getInstagramData(self):
		L = Instaloader()
		PROFILENAME='umcs_lublin'
		profile = Profile.from_username(L.context, PROFILENAME)
		itemList = [] 
		iter =0
		
		itemList.append({
			"followers": profile.followers
			})
		
		for post in profile.get_posts():
			iter += 1
			itemList.append({
				"id": iter,
				"photo_url": post.url,
				"caption": post.caption,
				"likes": post.likes
	        })
			if iter == 5:
				break
		return itemList

if __name__ == "__main__":
	start()
