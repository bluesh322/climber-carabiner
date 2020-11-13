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
from ..models import User, db, Route, Project, Send, Follows, Kudo, Likes
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
    b_levels = dict(boulder_levels)
    s_levels = dict(sport_levels)
    is_following = [follow.user_being_followed_id for follow in Follows.query.filter(
            Follows.user_following_id == current_user.id).all()]
    is_project = [project.route_id for project in Project.query.filter(Project.user_id == current_user.id).all()]
    followed_users = User.query.filter(User.id.in_(is_following)).limit(5).all()
    recent_projects = Project.query.filter(or_(Project.user_id.in_(is_following), Project.user_id == current_user.id)).order_by(Project.projected_on.desc()).limit(20).all()
    recent_sends = Send.query.filter(or_(Send.user_id.in_(is_following), Send.user_id == current_user.id)).order_by(Send.sent_on.desc()).limit(20).all()
    geo = func.ST_GeomFromText('POINT({} {})'.format(current_user.lon, current_user.lat))
    nearby_users = User.query.filter(and_(func.ST_DistanceSphere(User.geo, geo) < (50*1609.344), (User.id != current_user.id))).order_by(func.ST_DistanceSphere(User.geo, geo)).limit(5).all()
    nearby_routes = Route.get_routes_within_radius_count_for_feed(current_user.lat, current_user.lon, 500, 5)
    feed = generate_feed_from_users_and_routes(nearby_users, nearby_routes)

    return render_template(
        'user_feed.html',
        boulder_levels=b_levels, 
        sport_levels=s_levels,
        feed=feed,
        followed_users=followed_users,
        is_following=is_following,
        is_project=is_project,
        recent_projects=recent_projects,
        recent_sends=recent_sends)

@user_views.route('/user/view-profile/<int:id>')
@login_required
def show_user_profile(id):
    b_levels = dict(boulder_levels)
    s_levels = dict(sport_levels)
    if id == current_user.id:
        form=EditClimbInfo(obj=current_user)

        project_routes_ids = [project.route_id for project in Project.query.filter(Project.user_id == current_user.id).all()]
        projected_routes = Route.query.filter(Route.id.in_(project_routes_ids)).limit(5).all()
        send_routes_ids = [send.route_id for send in Send.query.filter(Send.user_id == current_user.id).all()]
        sent_routes = Route.query.filter(Route.id.in_(send_routes_ids)).limit(5).all()
        return render_template(
            'view_profile.html', 
            boulder_levels=b_levels, 
            sport_levels=s_levels, 
            form=form,
            projected_routes = projected_routes,
            sent_routes = sent_routes
            )
    else:
        user = User.query.get_or_404(id)
        project_routes_ids = [project.route_id for project in Project.query.filter(Project.user_id == id).all()]
        projected_routes = Route.query.filter(Route.id.in_(project_routes_ids)).limit(5).all()
        send_routes_ids = [send.route_id for send in Send.query.filter(Send.user_id == id).all()]
        sent_routes = Route.query.filter(Route.id.in_(send_routes_ids)).limit(5).all()

        return render_template(
            'view_other_user_profile.html',
            user=user,
            boulder_levels=b_levels, 
            sport_levels=s_levels,
            projected_routes = projected_routes,
            sent_routes = sent_routes
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
    if(user_location.geo):
        res = {'location': False}
        return jsonify(res=res)
    else:
        res = {'location': True}
        return jsonify(res=res)

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
def add_like_to_project(projet_id):
    """Add like for a user project"""
    is_liked = Likes.query.filter(
        and_(Likes.user_id == current_user.id, Likes.route_id == project_id)).first()
    if is_liked:
        # unlike project
        sess.delete(is_liked)
        sess.commit()
        return jsonify({msg:"unliked"})
    else:
        # like project
        new_like = Likes()
        new_like.user_id = current_user.id
        new_like.route_id = project_id
        sess.add(new_like)
        sess.commit()
        return jsonify({msg:"project liked"})

@user_views.route('/user/toggle_kudo/<int:send_id>', methods=["POST"])
@login_required
def add_kudo_to_send(send_id):
    """Add like for a user project"""
    is_kudoed = Kudo.query.filter(
        and_(Kudo.user_id == current_user.id, Kudo.route_id == send_id)).first()
    if is_liked:
        # unlike project
        sess.delete(is_liked)
        sess.commit()
        return jsonify({msg:"unliked"})
    else:
        # like project
        new_like = Kudo()
        new_like.user_id = current_user.id
        new_like.route_id = send_id
        sess.add(new_like)
        sess.commit()
        return jsonify({msg:"send kudo"})
    