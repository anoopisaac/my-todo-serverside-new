#!/usr/bin/env python

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from models import User

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
import urllib
import json
import hashlib
import time

SALT = "123-2343-abc&533"

def user_required(handler):
    """
      Decorator that checks if there's a user associated with the current session.
      Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login

class Utility:

    cookie_value = self.request.cookies.get('stay_logged')
        user_id

     @classmethod
    def is_user_logged_in(cls,response,user):
        stay_logged_hash=Utility.get_stay_loggedin_hash();
        cookie_value='{}:{}'.format(",".join(user.auth_ids), stay_logged_hash)
        response.set_cookie('stay_logged',cookie_value , max_age=360, path='/' )

    @classmethod
    def set_stay_logged_cookie(cls,response,user):
        stay_logged_hash=Utility.get_stay_loggedin_hash();
        cookie_value='{}:{}'.format(",".join(user.auth_ids), stay_logged_hash)
        response.set_cookie('stay_logged',cookie_value , max_age=360, path='/' )


    @classmethod
    def get_stay_loggedin_hash(cls):
        string_to_hash='{}:{}'.format(SALT, time.time())
        return hashlib.sha512( string_to_hash ).hexdigest()
    @classmethod
    def get_json_response(cls, url):
        """
        Parse the access token from Facebook's response
        Args:
            uri: the facebook graph api oauth URI containing valid client_id,
                redirect_uri, client_secret, and auth_code arguements
        Returns:
            a string containing the access key 
        """
        resp = str(urllib.urlopen(url).read()).encode("utf-8")
        json_resp = json.loads(resp)
        return json_resp;


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
          config['webapp2_extras.auth']['user_attributes'].
        :returns
          A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
          The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
            'message': message
        }
        self.render_template('message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
            # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)