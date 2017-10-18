#!/usr/bin/env python

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from models import User

from utility import BaseHandler
from utility import Utility


class MainHandler(BaseHandler):
    # def get(self):
    #     my_user=User.query(User.auth_ids == "anoopisaac@gmail.com").get()
    #     params = {
    #         'users': self.get_users(),
    #         'cls':User,
    #         'user1':my_user
    #     }
    #     self.render_template('login1.html',params)

    def get(self):
        self.render_template('home.html')

    def get_users(self):
        #user=User()
        qry = User.query()
        users = qry.fetch(20)       
        for user in users:
            logging.info(user.email_address)
            logging.info(','.join(user.auth_ids))

        return users