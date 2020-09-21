"""Compile static assets"""
from flask import current_app as app 
from flask_assets import Bundle

def compile_assets(assets):
    """Create stylesheet bundles"""
    assets.auto_build = True
    assets.debug = True

    index_css_bundle = Bundle(
        'index_bp/index.css',
        output='dist/css/index.css',
        extra={'rel':'stylesheet/css'}
    )
    user_views_css_bundle = Bundle(
        'user_views/user_views.css',
        output='gen/user_views.css',
        extra={'rel':'stylesheet/css'}
    )
    assets.register('index_css_bundle', index_css_bundle)
    assets.register('user_views_css_bundle', user_views_css_bundle)
    if app.config['FLASK_ENV'] == 'development':
        index_css_bundle.build()
    return assets