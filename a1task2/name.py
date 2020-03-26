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

class Name(webapp2.RequestHandler):
    def post(self):
        template_values = {
            'username':self.request.get('username'),
            'id':self.request.get('id'),
        }
        template = JINJA_ENVIRONMENT.get_template('name.html')
        self.response.write(template.render(template_values))

class ChangeName(webapp2.RequestHandler):
    def post(self):
        id = self.request.get('id')
        newusername = self.request.get('newusername')
        message = ''
        my_user = user.query(user.id==login_key(id)).fetch(1)
        username = ''

        if (newusername):
            #update user name
            my_user[0].name = newusername
            my_user[0].put()

            user_params = {
                'username':newusername,
                'id':id,
            }
            self.redirect('/main?' + urllib.urlencode(user_params))
        else:
            message = 'User name cannot be empty'
            username = my_user[0].name

        template_values = {
            'message':message,
            'id':id,
            'username':username,
        }

        template = JINJA_ENVIRONMENT.get_template('name.html')
        self.response.write(template.render(template_values))

# [START app]
app = webapp2.WSGIApplication([
    ('/name',Name),
    ('/changename',ChangeName),
], debug=True)
# [END app]
