

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

class User(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Login(webapp2.RequestHandler):
    def post(self):
        #require id and password
        id = self.request.get('id')
        password = self.request.get('password')
        message = ''
        id_check = user.query(user.id==login_key(id)).fetch(1)
        password = int(password)
        if (id_check):
            if (password == id_check[0].password):
                username = id_check[0].name
                user_params = {
                    'username':username,
                    'id':id,
                }
                self.redirect('/main?' + urllib.urlencode(user_params))

        message = 'User id or password is invalid'

        template_values = {
            'message':message,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/', User),
    ('/login',Login),
], debug=True)
# [END app]
