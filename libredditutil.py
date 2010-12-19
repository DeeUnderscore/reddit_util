#!/usr/bin/env python
# libredditutil.py
"""
Helper functions for reddit-util
"""

import sys
import urllib2
from datetime import timedelta, datetime
import json

def get_history(username, depth=60, kind='all'):
	"""
	Returns a reddit comment history for username
	
	depth - a cutoff for the age of comments that are included, in days. If 
		the comment list ends earlier than the cutoff, all comments will be returned
	kind - can be "comment", "sub". This function fetches either the comment
		history for a user, the submission (link) history, or a mix of the
		two as displayed on the main userpage (default behavior).
	"""
	
	# the format for userpage URL is
	# http://www.reddit.com/user/USERNAME/[TYPE].json[?after=NEXTSTRING]
	# TYPE can be either 'comments/' or 'submitted/'. If left out, we get the
	# default userpage
	# The after portion is used for pagination
	url = "http://www.reddit.com/user/" + username
	
	if kind == "comment":
		url += "/comments/.json"
	elif kind == "sub":
		url += "/submitted/.json"
	else:
		url += "/.json"
	# for reference, each item has a "kind" field, which is set to
	# "t1" for comments and "t3" for submissions
	
	next = ''
	current_time = datetime.utcnow()
	found_all = False
	return_list = []
	
	while not found_all:
		current_file = urllib2.urlopen(url + next)
		current_data = json.load(current_file)
		for item in current_data["data"]["children"]:
			time_diff = current_time - \
			            datetime.utcfromtimestamp(
			            item["data"]["created_utc"])
			
			if time_diff.days <= depth:
				return_list.append(item["data"])
			else:
				found_all = True
				break
		
		if current_data["data"]["after"]:
			next = "?after=" + current_data["data"]["after"]
		else:
			# if no next, we're at the end
			found_all = True
	
	return return_list
	
def get_about(username):
	"""
	Get the about.json data for a user
	"""
	
	url = "http://www.reddit.com/user/" + username + "/about.json"
	
	current_file = urllib2.urlopen(url)
	return json.load(current_file)["data"]
	