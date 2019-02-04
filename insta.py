"""
from instalooter.looters import ProfileLooter
looter = ProfileLooter("umcs_lublin", dump_json=True)
def downloadInstagram():
	looter.download('media/', media_count=5)

def links(media, looter):
    if media.get('__typename') == "GraphSidecar":
        media = looter.get_post_info(media['shortcode'])
        nodes = [e['node'] for e in media['edge_sidecar_to_children']['edges']]
        return [n.get('video_url') or n.get('display_url') for n in nodes]
    elif media['is_video']:
        media = looter.get_post_info(media['shortcode'])
        return [media['video_url']]
    else:
        return [media['display_url']]

if __name__ == "__main__":
	downloadInstagram()
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re
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