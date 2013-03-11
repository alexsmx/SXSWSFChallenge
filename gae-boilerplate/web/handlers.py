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
from google.appengine.api import taskqueue
from web import models as local_models


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

            url='https://api.angel.co/1/search?query=' + term + '&type=User'
            logging.info(url)
            response = urllib2.urlopen(url)
            json_data = response.read()
            logging.info('OJO: %s' % json_data)
            self.response.out.write( json_data)
        else:
            self.response.out.write('{}')

def getAngelProfile(id):
    url='https://api.angel.co/1/search?query=' + term + '&type=User'
    response = urllib2.urlopen(url)
    json_data = json.loads(response.read())
    return json_data

def getCrunchProfile(id):
    url= 'http://api.crunchbase.com/v/1/search.js?query=' + term + '&api_key=a3atu3g9gkmpfbcrdey8w6hz'
    response = urllib2.urlopen(url)
    json_data = json.loads(response.read())
    return json_data

class searchCrunchBaseHandler(BaseHandler):
    def get(self):
        term= self.request.get('terms').strip()
        if term !='':
            logging.info(urllib.quote(term))
            term= urllib.quote(term)
            url= 'http://api.crunchbase.com/v/1/search.js?query=' + term + '&api_key=a3atu3g9gkmpfbcrdey8w6hz&namespace=people'
            logging.info(url)
            response= urllib2.urlopen(url)
            json_data=response.read()
            logging.info('OJO: %s' % json_data)
            self.response.out.write( json_data)
        else:
            self.response.out.write('{}')

class addProfileHandler(BaseHandler):
    def get(self):
        source= self.request.get('source')
        id=self.request.get('id')
        if source.strip()=='' or id.strip()=='':
            pass
        else:
            add_profile_url = self.uri_for('add-task-profile')
            taskqueue.add(url = add_profile_url, params={
                'source': str(source),
                'id' : id,
                })


def getJsonUrlData(url1):
    logging.info(url1)
    response= urllib2.urlopen(url1)
    json_data = json.loads(response.read())
    return json_data
    
class addTaskProfileHandler(BaseHandler):
    def get(self):
        source= self.request.get('source')
        id=self.request.get('id')
        url1=''
        if source=='CrunchBase':
            pass
        elif source=='AngelList':
            url1='https://api.angel.co/1/users/' + id
            url2 = 'https://api.angel.co/1/users/' + id + '/startups'
            datoUsuario=getJsonUrlData(url1)
            datosStartups=getJsonUrlData(url2)
            roles=datosStartups['startup_roles']
            lista_startups_ids=[]
            lista_startups_nombres=[]
            for role in roles:
                #logging.info('%s %s %s %s %s' % (role['role'],role['startup']['id'], role['startup']['name'],role['started_at'],role['ended_at']))
                lista_startups_ids.append(role['startup']['id'])
                lista_startups_nombres.append(role['startup']['name'])
            #logging.info(lista_startups_ids)
            #logging.info(lista_startups_nombres)
            profile_ndb= local_models.ProfileData.query(local_models.ProfileData.identificador==id).fetch()
            if len(profile_ndb)==0:
                profile_ndb= local_models.ProfileData(source=source, identificador=id, name=datoUsuario['name'], location=json.dumps(datoUsuario['locations']),
                    tweeter_profile=datoUsuario['twitter_url'], startups_ids=json.dumps(lista_startups_ids), startups_nombres=json.dumps(lista_startups_nombres))
                profile_ndb.put()
        else:
            pass

class addTaskInvestorsHandler(BaseHandler):
    def get(self):
        source =self.request.get('source')
        id=self.request.get('id')
        url1=''
        if source=='CrunchBase':
            pass
        elif source=='AngelList':
            url2 = 'https://api.angel.co/1/users/' + id + '/startups'
            datosStartups=getJsonUrlData(url2)        
            for startup in datosStartups['startup_roles']:
                if startup['role']=='past_investor':
                    id_comp= startup['startup']['id']
                    profile_ndb= local_models.Company.query(local_models.Company.identificador==str(id_comp)).fetch()
                    if len(profile_ndb)==0:            
                        lista_investors_names=[]
                        url3 = 'https://api.angel.co/1/startup_roles?startup_id=' + str(startup['startup']['id'])
                        inversionistas= getJsonUrlData(url3)
                        for role in inversionistas['startup_roles']:
                            if role['role']=='past_investor':
                                logging.info(role['user']['name'])
                                lista_investors_names.append(role['user']['name'])
                        profile_ndb=local_models.Company(source=source, identificador=str(id_comp), name='test', investors=json.dumps(lista_investors_names) )
                        profile_ndb.put()


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


