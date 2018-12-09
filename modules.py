# -*- encoding: utf-8 -*- #
from google.appengine.ext import ndb

class GuestbookEntry( ndb.Model ):
    name = ndb.StringProperty()
    mail = ndb.StringProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)