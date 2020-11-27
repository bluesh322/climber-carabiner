from flask import (
    current_app,
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify
)
from ..models import User, db, Route, Project, Follows, Send, Kudos, Likes
from flask_login import login_required, current_user
from .user_forms import EditProfileForm, EditClimbInfo, boulder_levels, sport_levels
from sqlalchemy import and_, or_, func, asc
from random import sample
from .feed import generate_feed_from_users_and_routes
import datetime

sess = db.session

user_views = Blueprint(
    "user_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@user_views.route('/user-feed')
@login_required
def show_user_feed():
    b_levels = boulder_levels
    s_levels = sport_levels
    is_following = [follow.user_being_followed_id for follow in Follows.query.filter(
            Follows.user_following_id == current_user.id).all()]
    is_project = [project.route_id for project in Project.query.filter(Project.user_id == current_user.id).all()]
    is_send = [send.route_id for send in Send.query.filter(Send.user_id == current_user.id).all()]
    followed_users = User.query.filter(User.id.in_(is_following)).limit(5).all()
    recent_projects = Project.query.filter(or_(Project.user_id.in_(is_following), Project.user_id == current_user.id)).order_by(Project.projected_on.desc()).limit(20).all()
    recent_sends = Send.query.filter(or_(Send.user_id.in_(is_following), Send.user_id == current_user.id)).order_by(Send.sent_on.desc()).limit(20).all()
    geo = func.ST_GeomFromText('POINT({} {})'.format(current_user.lon, current_user.lat))
    nearby_users = User.query.filter(and_(func.ST_DistanceSphere(User.geo, geo) < (50*1609.344), (User.id != current_user.id), (User.id.notin_(is_following)))).order_by(func.ST_DistanceSphere(User.geo, geo)).limit(5).all()
    nearby_routes = Route.get_routes_within_radius_count_for_feed(current_user.lat, current_user.lon, 500, 5)
    feed = generate_feed_from_users_and_routes(nearby_users, nearby_routes)
    is_p = [project.id for project in Project.query.filter(Project.user_id == current_user.id).all()]
    is_liked = [like.project_id for like in Likes.query.filter(
        Likes.user_id == current_user.id).all()]
    kudos = [kudo.send_id for kudo in Kudos.query.filter(
        Kudos.user_id == current_user.id).all()]

    return render_template(
        'user_feed.html',
        boulder_levels=b_levels, 
        sport_levels=s_levels,
        feed=feed,
        followed_users=followed_users,
        is_following=is_following,
        is_project=is_project,
        is_send=is_send,
        recent_projects=recent_projects,
        recent_sends=recent_sends,
        is_liked=is_liked,
        kudos=kudos)

@user_views.route('/user/view-profile/<int:id>')
@login_required
def show_user_profile(id):
    b_levels = boulder_levels
    s_levels = sport_levels
    if id == current_user.id:
        form=EditClimbInfo(obj=current_user)

        project_routes_ids = [project.route_id for project in Project.query.filter(Project.user_id == current_user.id).all()]
        projected_routes = Route.query.filter(Route.id.in_(project_routes_ids)).all()
        project_routes = Project.query.filter(Project.user_id == current_user.id).all()
        sent_routes = Send.query.filter(Send.user_id == current_user.id).all()
        likes = [like.project_id for like in Likes.query.filter(
                Likes.user_id == current_user.id).all()]
        kudos = [kudo.send_id for kudo in Kudos.query.filter(
                Kudos.user_id == current_user.id).all()]

        return render_template(
            'view_profile.html', 
            boulder_levels=b_levels, 
            sport_levels=s_levels, 
            form=form,
            projected_routes = project_routes,
            sent_routes = sent_routes,
            likes=likes,
            kudos=kudos
            )
    else:
        user = User.query.get_or_404(id)
        project_routes_ids = [project.route_id for project in Project.query.filter(Project.user_id == id).all()]
        projected_routes = Route.query.filter(Route.id.in_(project_routes_ids)).all()
        send_routes_ids = [send.route_id for send in Send.query.filter(Send.user_id == id).all()]
        sent_routes = Route.query.filter(Route.id.in_(send_routes_ids)).all()
        likes = [like.project_id for like in Likes.query.filter(
                Likes.user_id == current_user.id).all()]
        kudos = [kudo.send_id for kudo in Kudos.query.filter(
                Kudos.user_id == current_user.id).all()]
        proj_route_ids = [route.id for route in projected_routes]
        projects = Project.query.filter(and_(Project.route_id.in_(proj_route_ids)), (Project.user_id == user.id)).all()
        sent_route_ids = [route.id for route in sent_routes]
        sends = Send.query.filter(and_((Send.route_id.in_(sent_route_ids)), (Send.user_id == user.id))).all()

        return render_template(
            'view_other_user_profile.html',
            user=user,
            boulder_levels=b_levels, 
            sport_levels=s_levels,
            projected_routes = projected_routes,
            sent_routes = sent_routes,
            likes=likes,
            kudos=kudos,
            projects=projects,
            sends=sends
        )

@user_views.route('/user/edit-profile', methods=["GET", "POST"])
@login_required
def edit_user_profile():
    user = User.query.get_or_404(current_user.id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.image_url = form.img_url.data
        user.username = form.username.data
        user.email = form.email.data
        user.b_skill_level = form.b_skill_level.data
        user.tr_skill_level = form.tr_skill_level.data
        user.ld_skill_level = form.ld_skill_level.data
        user.goals = form.goals.data
        user.location = form.location.data
        sess.add(user)
        sess.commit()
        return redirect(url_for("user_views.show_user_profile", id=current_user.id))
    else:
        return render_template('edit_profile.html', form=form)

@user_views.route('/user/list-connections', methods=["GET", "POST"])
def list_user_connections():
    return render_template('list_connections.html')

@user_views.route('/user/edit_goals', methods=["POST"])
@login_required
def edit_user_goals():
    form=EditClimbInfo()
    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        user.goals = form.goals.data
        user.b_skill_level = form.b_skill_level.data
        user.tr_skill_level = form.tr_skill_level.data
        user.ld_skill_level = form.ld_skill_level.data
        sess.add(user)
        sess.commit()
    return redirect(url_for("user_views.show_user_profile", id=current_user.id))

@current_app.login_manager.user_loader
def load_user(id):
    return User.query.get_or_404(int(id))

@user_views.route('/user/projects', methods=["GET"])
@login_required
def list_projects():
    """Get List of Projects for the Current User"""
    all_projects = [project.serialize() for project in Project.query.filter(Project.user_id == current_user.id).all()]
    return jsonify(projects=all_projects)

@user_views.route('/user/add_project_route/<int:rt_id>', methods=["POST"])
@login_required
def add_project_route(rt_id):
    """Toggle route to project list to user profile"""
    is_projected = Project.query.filter(
    and_(Project.user_id == current_user.id, Project.route_id == rt_id)).first()

    if is_projected:
        # unproject
        sess.delete(is_projected)
        sess.commit()
        project = is_projected.serialize()
        return jsonify(is_projected=project)
    else:
        # add project
        new_proj = Project()
        new_proj.user_id = current_user.id
        new_proj.route_id = rt_id
        new_proj.projected_on = datetime.datetime.now()
        sess.add(new_proj)
        sess.commit()
        project = new_proj.serialize()
        return jsonify(is_projected=project)

@user_views.route('/user/sends', methods=["GET"])
@login_required
def list_sends():
    """Get List of Projects for the Current User"""
    all_sends = [send.serialize() for send in Send.query.filter(Send.user_id == current_user.id).all()]
    return jsonify(sends=all_sends)

@user_views.route('/user/add_sent_route/<int:rt_id>', methods=["POST"])
@login_required
def add_sent_route(rt_id):
    """Add route to sent list to user profile"""
    is_sent = Send.query.filter(
    and_(Send.user_id == current_user.id, Send.route_id == rt_id)).first()
    is_projected = Project.query.filter(
    and_(Project.user_id == current_user.id, Project.route_id == rt_id)).first()
    if is_projected:
        sess.delete(is_projected)
        sess.commit()
    if is_sent:
        # unsend
        sess.delete(is_sent)
        sess.commit()
        sent = is_sent.serialize()
        return jsonify(sent=sent)
    else:
        # add project
        new_send = Send()
        new_send.user_id = current_user.id
        new_send.route_id = rt_id
        new_send.attempts = request.json.get('attempts', new_send.attempts)
        new_send.sent_on = datetime.datetime.now()
        sess.add(new_send)
        sess.commit()
        sent = new_send.serialize()
        return jsonify(sent=sent)

@user_views.route('/user/location')
@login_required
def is_user_location():
    """Check if the user geo location set"""
    user_location = User.query.get_or_404(current_user.id)
    print("************************")
    print(user_location.lat)
    print(user_location.lon)
    print(user_location.geo)
    if user_location.geo is not None:
        print("********************")
        print("STILL GOING HERE")
        return redirect(url_for("user_views.show_user_feed"))
    else:
        print("******************")
        print("GOING HERE")
        return render_template("location.html")

@user_views.route('/user/location', methods=["POST"])
@login_required
def set_user_location():
    """Set user location, geo, lat, and long"""
    req = request.json
    user = User.query.get_or_404(current_user.id)
    user.lat = req.get('lat')
    user.lon = req.get('lon')
    user.location = req.get('location')
    print(user.lat)
    print(user.lon)
    print(user.location)
    user.geo = 'POINT({} {})'.format(user.lon, user.lat)
    sess.add(user)
    sess.commit()
    user = user.serialize()
    return jsonify(user=user)

@user_views.route('/user/add_connection/<int:follow_id>', methods=["POST"])
@login_required
def add_connection(follow_id):
    """Add user connection for a user"""
    followed_user = User.query.get_or_404(follow_id)
    current_user.following.append(followed_user)
    sess.commit()
    user = current_user.serialize()

    return jsonify(user=user)

@user_views.route('/user/rem_connection/<int:follow_id>', methods=["POST"])
@login_required
def rem_connection(follow_id):
    """Remove user connection for a user"""
    followed_user = User.query.get_or_404(follow_id)
    current_user.following.remove(followed_user)
    sess.commit()
    user = current_user.serialize()

    return jsonify(user=user)

@user_views.route('/user/toggle_like/<int:project_id>', methods=["POST"])
@login_required
def add_like_to_project(project_id):
    """Add like for a user project"""
    is_liked = Likes.query.filter(
        and_(Likes.user_id == current_user.id, Likes.project_id == project_id)).first()
    if is_liked:
        # unlike project
        sess.delete(is_liked)
        sess.commit()
        return jsonify(msg="unliked")
    else:
        # like project
        new_like = Likes()
        new_like.user_id = current_user.id
        new_like.project_id = project_id
        sess.add(new_like)
        sess.commit()
        return jsonify(msg="project liked")

@user_views.route('/user/toggle_kudo/<int:send_id>', methods=["POST"])
@login_required
def add_kudo_to_send(send_id):
    """Add like for a user project"""
    is_kudoed = Kudos.query.filter(
        and_(Kudos.user_id == current_user.id, Kudos.send_id == send_id)).first()
    if is_kudoed:
        # unlike project
        sess.delete(is_kudoed)
        sess.commit()
        return jsonify(msg="unliked")
    else:
        # like project
        new_kudo = Kudos()
        new_kudo.user_id = current_user.id
        new_kudo.send_id = send_id
        sess.add(new_kudo)
        sess.commit()
        return jsonify(msg="send kudo")

@user_views.route('/user/connections_list/<int:user_id>', methods=["GET"])
@login_required
def show_connection_list(user_id):
    """Show all the connections a user has"""
    user = User.query.get_or_404(user_id)
    return render_template('connection_list.html', user=user, boulder_levels=boulder_levels, sport_levels=sport_levels)

@user_views.route('/user/projects_list/<int:user_id>', methods=["GET"])
@login_required
def show_project_list(user_id):
    """Show all the connections a user has"""
    user = User.query.get_or_404(user_id)
    routes = Project.query.filter(Project.user_id == user_id).all()
    likes = [like.project_id for like in Likes.query.filter(
            Likes.user_id == current_user.id).all()]
    route_ids = [route.id for route in routes]
    return render_template(
        'project_list.html',
        user=user, 
        projected_routes=routes, 
        likes=likes)

@user_views.route('/user/sends_list/<int:user_id>', methods=["GET"])
@login_required
def show_send_list(user_id):
    """Show all the connections a user has"""
    user = User.query.get_or_404(user_id)
    send_ids = [send.route_id for send in Send.query.filter(Send.user_id == user_id).all()]
    routes = Route.query.filter(Route.id.in_(send_ids)).all()
    kudos = [kudo.send_id for kudo in Kudos.query.filter(
            Kudos.user_id == current_user.id).all()]
    route_ids = [route.id for route in routes]
    sends = Send.query.filter(Send.route_id.in_(route_ids)).all()
    return render_template('send_list.html', user=user, sent_routes=routes, kudos=kudos, sends=sends)
    