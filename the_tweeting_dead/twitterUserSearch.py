import urllib
import json
import oauth2 as oauth
import urllib2 as urllib

#you'll need to get these by registering for your own twitter developer account
api_key = "***"
api_secret = "***"
access_token_key = "***"
access_token_secret = "***"

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=0)
https_handler = urllib.HTTPSHandler(debuglevel=0)

def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer, token=oauth_token, http_method=http_method, http_url=url, parameters=parameters)
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
    url = req.to_url()
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    response = opener.open(url, encoded_post_data)
    return response

def main():
    url = "https://stream.twitter.com/1.1/statuses/filter.json?track=MakeAmericaMoreAmerican&locations=-123.0,46.96,-121.96,47.85"
    pars = []
    response = twitterreq(url, "GET", pars)
    for line in response:
      print line.strip()

if __name__ == '__main__':
  main()