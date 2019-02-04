import json
import requests
from instaloader import Instaloader, Profile

L = Instaloader()
PROFILE='umcs_lublin'
profile = Profile.from_username(L.context, PROFILE)


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