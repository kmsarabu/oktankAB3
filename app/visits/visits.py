import os
from pymemcache.client import base
from flask import session, redirect, escape, request

visits_bp = Blueprint("visits_bp", __name__, template_folder="templates/visits")

client = base.Client( ('ab3ec.qkhr2o.cfg.use1.cache.amazonaws.com', 11211) )

@app.route('/visits')
def index():
  if session and 'email' in session:
     username = escape(session['username'])
     visits = client.hincrby(username, 'visits', 1)
  return '''
        Logged in as {0}.<br>
        Visits: {1}
        '''.format(username, visits)
