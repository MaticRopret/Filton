# -*- encoding: utf-8 -*- #
#!/usr/bin/env python

import os
import jinja2
import webapp2

from modules import GuestbookEntry


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))



class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class AddMessageHandler(BaseHandler):
    def post(self):
        name = self.request.get("name")
        mail = self.request.get("mail")
        content = self.request.get("content")

        if not name:
            name = "Neznanec"
        if not mail:
            mail = "Neznani e-mail naslov"


        guestbookentry_post = GuestbookEntry( name=name, mail=mail, content=content )
        guestbookentry_post.put()

        return self.redirect_to("sporocila")


class ShowGuestbookHandler(BaseHandler):
    def get(self):
        vnosi = GuestbookEntry.query().fetch()

        params = {
            "vnosi": vnosi
        }

        return  self.render_template( "messages.html", params=params)

class ShowSingleGuestbookEntryHandler( BaseHandler ):
    def get(self, id ):
        vnos = GuestbookEntry.get_by_id(int( id ))
        params = {
            "vnos": vnos
        }
        return self.render_template( "message.html", params=params)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/addmessage', AddMessageHandler),
    webapp2.Route('/messages', ShowGuestbookHandler, name="sporocila"),
    webapp2.Route('/message/<id:\d+>', ShowSingleGuestbookEntryHandler)

], debug=True)
