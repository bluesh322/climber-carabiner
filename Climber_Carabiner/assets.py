"""Compile static assets"""
from flask import current_app as app 
from flask_assets import Bundle

def compile_assets(assets):
    """Create stylesheet bundles"""
    assets.auto_build = True
    assets.debug = False

    user_views_css_bundle = Bundle(
        'user_views/user_views.css',
        output='gen/user_views.css',
        extra={'rel':'stylesheet/css'}
    )
    search_js = Bundle(
        'search_views/search.js',
        output='gen/search.js',
        filters='jsmin'
    )
    search_css = Bundle(
        'search_views/search.css',
        output='gen/search.css',
        filters='cssmin'
    )

    # auth_css = Bundle(
    #     'auth_bp/auth.css',
    #     output='gen/auth.css',
    #     filters='cssmin'
    # )

    auth_js = Bundle(
        'auth_bp/auth.js',
        output='gen/auth.js',
        filters='jsmin'
    )

    view_profile_js = Bundle(
        'user_views/view_profile.js',
        output='gen/user_views.js',
        filters='jsmin'
    )

    user_feed_js = Bundle(
        'user_views/user_feed.js',
        output='gen/user_feed.js',
        filters='jsmin'
    )

    route_details_js = Bundle(
        'route_views/route_details.js',
        output="gen/route_views.js",
        filters='jsmin'
    )

    assets.register('user_views_css_bundle', user_views_css_bundle)
    assets.register('search_js', search_js)
    assets.register('search_css', search_css)
    # assets.register('auth_css', auth_css)
    assets.register('auth_js', auth_js)
    assets.register('view_profile_js', view_profile_js)
    assets.register('route_details_js', route_details_js)
    assets.register('user_feed_js', user_feed_js)
    if app.config['FLASK_ENV'] == 'development':
        search_js.build()
        search_css.build()
        # auth_css.build()
        auth_js.build()
        view_profile_js.build()
        route_details_js.build()
        user_feed_js.build()
    return assets