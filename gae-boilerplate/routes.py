"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers
from web import angellist
secure_scheme = 'https'

_routes = [
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/admin/home/', handlers.adminHomeHandler, name='admin-home', strict_slash=True),
    RedirectRoute('/admin/search/', handlers.adminSearchHandler, name='admin-search', strict_slash=True),
    RedirectRoute('/searchAngel/', handlers.searchAngelHandler, name='searchAngelHandler', strict_slash=True),
    RedirectRoute('/searchCrunch/', handlers.searchCrunchBaseHandler, name='searchCrunchHandler', strict_slash=True),
    
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)