# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_NAME = 'default_user'

def login_key(login_name=DEFAULT_NAME):
    """
    Constructs a Datastore key for an entity.
    We use login_name as the key.
    """
    return ndb.Key('user', login_name)

# [START greeting]
class user(ndb.Model):
    """model for representing an user."""
    id = ndb.KeyProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    password = ndb.IntegerProperty(indexed=False)

class Password(webapp2.RequestHandler):
    def post(self):
        template_values = {
            'username':self.request.get('username'),
            'id':self.request.get('id'),
        }
        template = JINJA_ENVIRONMENT.get_template('password.html')
        self.response.write(template.render(template_values))

class ChangePassword(webapp2.RequestHandler):
    def post(self):
        id = self.request.get('id')
        oldpassword = self.request.get('oldpassword')
        oldpassword = int(oldpassword)
        newpassword = self.request.get('newpassword')
        newpassword = int(newpassword)
        message = ''
        my_user = user.query(user.id==login_key(id)).fetch(1)

        if (oldpassword == my_user[0].password):
            my_user[0].password = newpassword
            my_user[0].put()

            self.redirect('/')
        else:
            message = 'User password is incorrect'

        template_values = {
            'message':message,
            'id':id
        }

        template = JINJA_ENVIRONMENT.get_template('password.html')
        self.response.write(template.render(template_values))

# [START app]
app = webapp2.WSGIApplication([
    ('/password',Password),
    ('/changepassword',ChangePassword),
], debug=True)
# [END app]
