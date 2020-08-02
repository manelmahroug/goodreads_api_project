try:
    import pprint
    import os
    import xml.etree.ElementTree as ET
    import json
    import requests
    from rauth.service import OAuth1Service, OAuth1Session
except Exception as e:
    print("\t", e)


def main():

    # Get a real consumer key & secret from: https://www.goodreads.com/api/keys
    CONSUMER_KEY = 'OKwj2qRaOnsUBJqogIu8tw'
    CONSUMER_SECRET = 'SJaIMqMXnskoF7Tlabf63WkbaADRCWt0ZmeREIohow'

    goodreads = OAuth1Service(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        name='goodreads',
        request_token_url='https://www.goodreads.com/oauth/request_token',
        authorize_url='https://www.goodreads.com/oauth/authorize',
        access_token_url='https://www.goodreads.com/oauth/access_token',
        base_url='https://www.goodreads.com/friend/user/24347448?format=xml'
    )

    # head_auth=True is important here; this doesn't work with oauth2 for some reason
    request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

    authorize_url = goodreads.get_authorize_url(request_token)
    print ('Visit this URL in your browser: ' + authorize_url)
    accepted = 'n'
    while accepted.lower() == 'n':
        # you need to access the authorize_link via a browser,
        # and proceed to manually authorize the consumer
        accepted = input('Have you authorized me? (y/n) ')


if __name__ == "__main__":
    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')

    main()
    input("\n\n\nPress enter to exit 🚀...")

    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')
