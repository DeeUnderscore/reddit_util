#!/usr/bin/env python
# karmas.py
"""Gather highly relevant data about a reddit user's karma
"""
from libredditutil import * 

def karmas(username, depth=None, kind="sub"):
	"""
	Returns an array of karma values for a user's items
	
	This is a wrapper around karmas_data()
	
	Parameters:
		kind - can either be "sub" or "comment", for link or comment karmas
		depth - the day count of how far back to look. If undefined, the default
			value in get_history() will be used.
	"""
	
	if kind != "sub" and kind != "comment":
		raise Exception("Invalid kind specified.")
	
	data = get_history(username, depth, kind)
	
	return karmas_data(data, kind)
	
def karmas_data(data, kind="sub"):
	"""
	Returns an array of karma values for a user's items
	
	Parameters:
		data - an array of user's items
		kind - either "sub" or "comment"
	"""

	score_list = []
	
	if kind == "sub":
		for item in data: score_list.append(item["score"])
	elif kind == "comment":
		# comments don't have a "score" field
		for item in data:
			score = item["ups"] - item["downs"]
			score_list.append(score)
	
	return score_list

	
def karma_velocity(username=None, kind="sub"):
	"""
	Determines the karma velocity of a given user
	
	See karma_velocity_data() for details.
	
	Parameters:
		kind - can be "sub" or "comment"
	"""
	if kind != "sub" and kind != "comment":
		raise Exception("Invalid kind specified.")
	
	return karma_velocity_data(get_about(username),kind)
	

def karma_velocity_data(data, kind="sub"):
	"""
	Determines a user's karma velocity
	
	Karma velocity is measured in karma per day. It is calculated by taking the
	user's karma count and dividing it by the age of account, in days.
	
	Parameters:
		data - a dictionary representation of the data contained in the 
			about.json file under the "data" field. 
	"""
	
	account_age = ( datetime.utcnow() -
	                datetime.utcfromtimestamp(data["created_utc"]) ).days
	
	if kind == "sub":
		return (data["link_karma"] / float(account_age))
	else:
		return (data["comment_karma"] / float(account_age))