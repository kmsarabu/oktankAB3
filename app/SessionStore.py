import memcache
import os
import json

class Sessionstore:
    """Store session data in Memcached."""

    def __init__(self, session_id):
        echosts = [ x.split(':')[0] for x in os.environ.get('ECHOST').split(',') ]
        self.sess = memcache.Client( echosts )
        self.sessid = session_id

    def set(self, key, value):
        return self.sess.set(self.sessid + ':' + key, value)

    def get(self, key):
        return self.sess.get(self.sessid + ':' + key)

