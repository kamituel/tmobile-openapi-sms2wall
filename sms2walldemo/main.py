 #!/usr/bin/env python

execfile("header.py")

class MainHandler(webapp.RequestHandler):
   def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))
	
   def post(self):
        msisdn = self.request.get("msisdn").replace("+", "").replace(" ", "")
        self.redirectToFacebook(self_addr % msisdn)

   def redirectToFacebook(self, self_addr):
        dialog_url = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=read_stream,xmpp_login,publish_stream,offline_access"
        dialog_url = dialog_url % (fcb_appid, urllib.quote(self_addr))
        self.response.out.write("<script> top.location.href='%s' </script>" % dialog_url)
	
class FacebookHandler(webapp.RequestHandler):
    def get(self):
        client_id = self.request.get("msisdn")
        code = self.request.get("code")

	token = self.getFacebookToken(code, self_addr % client_id)
        if token is None:
            self.response.out.write("Facebook auth failed")
            return
	
	logging.debug("Got Facebook token for "+client_id+": "+token)
	
	client = None
        clients = db.GqlQuery("SELECT * FROM Client WHERE msisdn = :1", client_id).fetch(1)
	if len(clients) > 0:
		client = clients[0]
		client.facebook_token = token
	else:
		client = Client(msisdn=client_id, facebook_token=token)
		
	client.put()
	
	path = os.path.join(os.path.dirname(__file__), 'confirm.html')
        self.response.out.write(template.render(path, {}))

    def getFacebookToken(self, code, self_addr):
        token_url = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (fcb_appid, urllib.quote(self_addr), fcb_secret, code)
	logging.debug("Getting Facebook token: "+token_url)
        resp = urlfetch.fetch(url = token_url)
        if resp.status_code <= 201:
	    return cgi.parse_qs(resp.content)["access_token"][0]
	
	logging.error("Getting Facebook token failed with status "+str(resp.status_code)+": "+resp.content)
        return None
	
def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/facebook', FacebookHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()