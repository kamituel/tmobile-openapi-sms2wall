#!/usr/bin/env python

execfile("header.py")
	
class SmsHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("ok")
		
	def post(self):
		self.response.out.write(self.request.body)
		body = json.loads(self.request.body)["api"]["request"]["messaging"]
		logging.debug("okay, got sms from ..%s.. to ..%s.. with text ..%s.." % (body["sender"], body["recepient"], body["text"]))
		
		sender = body["sender"]
		text = body["text"]
		
		logging.debug("searching for ::%s::" % sender)
		
		query = Client.all()
		query.filter("msisdn = ", str(sender))
		clients = query.fetch(1)

		if len(clients) == 1:
			self.postToWall(clients[0].facebook_token, text)
		else:
			logging.debug("zero or more than one client")
		
	def postToWall(self, token, text):
		logging.debug("Will post to Facebook Wall with token: "+token)
		
		post_url = "https://graph.facebook.com/me/feed"
		fields = {
			"access_token": token,
			"message": text
			}
		response = urlfetch.fetch(url=post_url, method=urlfetch.POST, payload=urllib.urlencode(fields))
		logging.debug("Status code: %s. Result: %s, text: %s, fcb_token: %s" % (response.status_code, response.content, text, token))  
	
def main():
    application = webapp.WSGIApplication([('/openapi/sms', SmsHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
