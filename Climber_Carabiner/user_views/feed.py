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

