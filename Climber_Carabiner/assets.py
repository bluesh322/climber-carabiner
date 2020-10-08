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

    assets.register('user_views_css_bundle', user_views_css_bundle)
    assets.register('search_js', search_js)
    assets.register('search_css', search_css)
    if app.config['FLASK_ENV'] == 'development':
        search_js.build()
        search_css.build()
    return assets