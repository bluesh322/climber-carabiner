from flask import current_app
from random import sample
from flask_login import current_user

def generate_feed_from_users_and_routes(users, routes):
    feed = set()

    for user in users:
        feed.add(user)
    
    for route in routes:
        feed.add(route)
    
    return sample(feed, len(feed))

def generate_feed_from_projects_sends(projects, sends):
    feed = set()

    for project in projects:
        feed.add(project)
    
    for send in sends:
        feed.add(send)
    
    return feed