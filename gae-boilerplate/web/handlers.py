# -*- coding: utf-8 -*-

"""
    A real simple app for using webapp2 with auth and session.

    It just covers the basics. Creating a user, login, logout
    and a decorator for protecting certain handlers.

    Routes are setup in routes.py and added in main.py
"""
import httpagentparser
import logging
import json
import urllib, urllib2
from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required


class SecureRequestHandler(BaseHandler):
    """
    Only accessible to users that are logged in
    """

    @user_required
    def get(self, **kwargs):
        user_session = self.user
        user_session_object = self.auth.store.get_session(self.request)

        user_info = models.User.get_by_id(long( self.user_id ))
        user_info_object = self.auth.store.user_model.get_by_auth_token(
            user_session['user_id'], user_session['token'])

        try:
            params = {
                "user_session" : user_session,
                "user_session_object" : user_session_object,
                "user_info" : user_info,
                "user_info_object" : user_info_object,
                "userinfo_logout-url" : self.auth_config['logout_url'],
                }
            return self.render_template('secure_zone.html', **params)
        except (AttributeError, KeyError), e:
            return "Secure zone error:" + " %s." % e

class adminHomeHandler(BaseHandler):
    def get(self):
        params={}
        return self.render_template('adminhome.html',**params)

class adminSearchHandler(BaseHandler):
    def get(self):
        params={}
        self.render_template('adminsearch.html',**params)

class searchAngelHandler(BaseHandler):
    def get(self):
        term=self.request.get('terms').strip()
        if term != '':
            logging.info(urllib.quote(term))
            term= urllib.quote(term)

            url='https://api.angel.co/1/search?query=' + term + ''
            logging.info(url)
            response = urllib2.urlopen(url)
            json_data = response.read()
            logging.info('OJO: %s' % json_data)
            self.response.out.write( json_data)
        else:
            self.response.out.write('{}')

class searchCrunchBaseHandler(BaseHandler):
    def get(self):
        term= self.request.get('terms').strip()
        if term !='':
            logging.info(urllib.quote(term))
            term= urllib.quote(term)
            url= 'http://api.crunchbase.com/v/1/search.js?query=' + term + '&api_key=a3atu3g9gkmpfbcrdey8w6hz'
            logging.info(url)
            response= urllib2.urlopen(url)
            json_data=response.read()
            logging.info('OJO: %s' % json_data)
            self.response.out.write( json_data)
        else:
            self.response.out.write('{}')

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]
    
