class authentication:
    """ This is where you put your secret stuff to authenticate your app on Twitter """
    def __init__(self):
        # Go to http://apps.twitter.com and create an app.
        # The consumer key and secret will be generated for you after
        self.consumer_key =""
        self.consumer_secret=""

        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        self.access_token=""
        self.access_token_secret=""

    def getconsumer_key(self):
        return self.consumer_key
    def getconsumer_secret(self):
        return self.consumer_secret
    def getaccess_token(self):
        return self.access_token
    def getaccess_token_secret(self):
        return self.access_token_secret