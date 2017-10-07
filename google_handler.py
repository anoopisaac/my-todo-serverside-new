#!/usr/bin/env python

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2
from google.appengine.api import users

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError


from utility import BaseHandler
from utility import Utility


class GoogleHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            logging.critical('This is a critical message::'+(users.get_current_user().user_id()))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        user_data = self.user_model.create_user(user.user_id(),
                                                    None,
                                                    email_address=user.email(), name="test",
                                                    last_name="last_name", verified=True)
        if not user_data[0]:  # user_data is a tuple
            logging.warning("insdie ifff.... data %r...%r",user_data[0],user_data[1]) 
            self.display_message('Unable to create user for email %s because of \
            duplicate keys %s' % ("user_name", user_data[1]))
            return
        #logging.warning("user data %r",user_data) 
        logging.warning("outside ifff.... data %r...%r",user_data[0],user_data[1]) 
        self.auth.set_session(
        self.auth.store.user_to_dict(user_data[1]), remember=True)
        logging.info("user in sesion %r  user %r url...%s",self.auth.get_user_by_session(),user,url)
        self.display_message('in google login page.')
        # user_name = profile_resp['email']
        # email = profile_resp['email']
        # name = profile_resp['email']
        # last_name = profile_resp['email']

        # user_data = self.user_model.create_user(user_name,
        #                                         unique_properties,
        #                                         email_address=email, name=name, password_raw=password,
        #                                         last_name=last_name, verified=False)
        # self.auth.set_session(
        #     self.auth.store.user_to_dict(user_data[1]), remember=True)
