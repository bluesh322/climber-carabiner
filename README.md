# Climber-Carabiner

[Proposal link](https://docs.google.com/document/d/14DqRuug4R3GVKoXW3sr0nLj0K2qU7WWp4MPSYB37G10/edit?usp=sharing)

# climbing-carabiner.herokuapp.com

## What is the purpose of my website?

I wanted to leverage the Mountain Project API and Google Maps API to help climbers find routes near them, and climbers near them with similar goals so they get together and climb routes with climbers they otherwise wouldn't know. 

## Features Implemented

- Sign Up/Login

Users natually needed to have persistent data between visits to the website to hold their connects, route info, projects, and sends information. I also only wanted users who confirmed their email to have access to searching due to caps with google maps api.

- User Feed

Like other social media type sites I wanted users to be shown nearby routes and users based in a feed consisting of users they connected with or routes they were interested in. 

- Edit Profile

- Connect / Like / Kudos

These are the ways users can interact with one another. A like for a friend projecting a route, and a kudo for if a friend sends the route.
A similar project could indicate to each user to try and make a trip to send the route or go work on it.

- Search Routes

Enable for climbers to find routes, but then also find other routes near those routes to climb. I also wanted users to be able to manually find friends to connect with, and for the moment it felt like the easiest way to implement that search. 

## User Flow

- A user would "Sign Up" from the homepage, add their credentials and be notified to check their email for a confirmation, and be redirected to the Login page. Once their email has been confirmed, they would be able to login.

- On login, you would see your user-feed, which should populate with routes nearby, users nearby, and show some incomplete profile information. 

- Users can then go to the Profile and edit their climber ability and further edit their profile with a profile picture, and goals.

- The user-feed would be available to begin viewing nearby routes, which could be projected or sent by the user and added to their profile. Other users can be seen in the feed and connected to as well. 

- If you view another users profile, you can view their recent projects/sends, and their goals. On each project/send, you could leave a like or kudo. 

- If you check out a route, you would see other routes near that route, and recent updates on the routes projects or sends by other users. The Mountain Project API, gives sparse information about the routes, so there could be a way to have users help add information about a route later on. 

- A user can also go to the search, and would have a google map, display their most recent sign in location, and show the user nearby routes on the map. As well as give the user some search options.

- If a user searches for a particular route by name, only routes containing the letters of the search will appear. A blank search will search for all routes currently. The search result, as well as resulting nearby routes will be displayed below the map in a list.

- Clicking the advanced checkbox enables all of the advanced search criteria, which are route type, distance from user, and difficulty low and high range. 

- Users can also browse for routes in an area by moving the map to that location as routes will populate by dragging the map. There is currently no filter for this feature.

- A user can also search other users by clicking the "Users radio button", will be switched to a different set of Advanced criteria. A blank search will look for all users, and any user containing the letters of the search will be found. As well for some refinement I implemented an Advanced distance filter to make sure the users are nearby.

## Tech Stack

- Python, Flask, Jinja, Javascript, and Postgres.

- Flask-Blueprints, Flask-Mail, Flask-Login, Flask-WTF, Flask-SQLAlchemy, Flask-Assets, bcrypt, 

- Jquery, Google Maps API, Mountain Project API.

- Postgis -- Enabled search in the database for location based data.

