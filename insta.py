import json
import requests
from instaloader import Instaloader, Profile

L = Instaloader()
PROFILE='umcs_lublin'
profile = Profile.from_username(L.context, PROFILE)
# TO DO:
# 1. Parse data to json
# 2. Exchange this to a class
# 3. Add async job schedule in app.py

def getFollowers():
	print(profile.followers)

def getPosts(number):
	iter =0
	for post in profile.get_posts():
		print(post.url)
		iter += 1
		if iter == number:
			break

if __name__ == "__main__":
	getFollowers()
	getPosts(5)