import time
from pprint import pprint
import requests

class Tinker():

    def __init__(self):

        params = {
            'context_id': 'asdf',
            'user_id': 'asdfasdf',
            'lis_person_contact_email_primary': 'davo@packback.co',
            'lis_person_name_given': '',
            'lis_person_name_family': '',
            'roles': 'Instructor',

            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': '1.0',

            'lti_message_type': 'basic-lti-launch-request',
            'lti_version': 'LTI-1p0'
        }

        token = oauth.Token(key="lti1_3c183712f49bc6e9df6c4430085791abb85dd9f39bcf8ae04d32967f0182cf1a", secret="f2503f881e5d919710dd13be3ca054bdac3df43fac11936ad16928d8fd54deee")
        consumer = oauth.Consumer(key="lti1_3c183712f49bc6e9df6c4430085791abb85dd9f39bcf8ae04d32967f0182cf1a", secret="f2503f881e5d919710dd13be3ca054bdac3df43fac11936ad16928d8fd54deee")

        # Set our token/key parameters
        # params['oauth_token'] = token.key
        params['oauth_consumer_key'] = consumer.key

        # Create our request. Change method, etc. accordingly.
        req = oauth.Request(method="GET", url='http://pb-prdalt-lmsapi.azurewebsites.net/lti/launch', parameters=params)

        # Sign the request.
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)

        params['oauth_body_hash'] = req.get_parameter('oauth_body_hash')
        params['oauth_signature'] = req.get_parameter('oauth_signature')
        params['oauth_signature_method'] = req.get_parameter('oauth_signature_method')
        params['oauth_token'] = req.get_parameter('oauth_token')

        pprint(params)

class MakeRequest():

    def __init__(self):

        url = 'https://dev-lms-api.packback.co/lti/launch'

        params = {
            'context_id': 'asdf',
            'user_id': 'asdfasdf',
            'lis_person_contact_email_primary': 'davo@packback.co',
            'lis_person_name_given': '',
            'lis_person_name_family': '',
            'roles': 'Instructor',
            'resource_link_id': '3asd',

            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': '1.0',
            'oauth_callback': 'about:blank',

            'lti_message_type': 'basic-lti-launch-request',
            'lti_version': 'LTI-1p0'
        }

        consumer = oauth.Consumer(key="12345", secret="secret")

        params['oauth_consumer_key'] = consumer.key

        # Create our request. Change method, etc. accordingly.
        req = oauth.Request(method="POST", url=url, parameters=params)

        # Sign the request.
        signature_method = oauth.SignatureMethod_HMAC_SHA1()

        req.sign_request(signature_method, consumer, None)

        response = requests.post(url, data=req)

MakeRequest()
