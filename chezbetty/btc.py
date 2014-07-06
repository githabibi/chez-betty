
import urllib
import time
import json
import hashlib
import hmac
from decimal import Decimal


class BTCException(Exception):
    pass

class Bitcoin(object):

    COINBASE_API_KEY = ""
    COINBASE_API_SECRET = ""

    HOSTNAME = ''

    def __init__(self, umid=None):
        self.umid = umid
        pass

    @staticmethod
    def req(url, body=None):
        try:
            opener = urllib.request.build_opener()
            nonce = int(time.time() * 1e6)
            message = str(nonce) + url + ('' if body is None else body)
            signature = hmac.new(bytes(Bitcoin.COINBASE_API_SECRET, "utf-8"),
                                 bytes(message, "utf-8"),
                                 hashlib.sha256).hexdigest()
            opener.addheaders = [('ACCESS_KEY', Bitcoin.COINBASE_API_KEY),
                                ('ACCESS_SIGNATURE', signature),
                                ('ACCESS_NONCE', nonce)]

            # is this really how you do this in this language?
            body_b = None
            if body is not None:
                body_b = bytes(body, "utf-8")

            res_s = opener.open(urllib.request.Request(url,
                body_b, {'Content-Type': 'application/json'})).read()
            return json.loads(str(res_s, 'utf-8'))

        except urllib.error.HTTPError as e:
            raise BTCException("Could not load HTTP")


    @staticmethod
    def get_new_address(umid="", cb_url='http://{}/bitcoin/deposit', guid='chezbetty'):

        cb_url = cb_url.format(Bitcoin.HOSTNAME)

        obj = Bitcoin.req("https://coinbase.com/api/v1/account/generate_receive_address",
                      '{"address": {"callback_url": "%s/%s", "label": "%s"}' % (cb_url, umid, guid))

        if not(obj['success']):
            raise BTCException("Could not get address: %s" % res)

        return obj['address']

    @staticmethod
    def get_spot_price(currency="USD"):
        obj = Bitcoin.req("https://coinbase.com/api/v1/prices/spot_rate?currency=%s" % currency)
        return Decimal(obj['amount'])

    @staticmethod
    def get_balance():
        obj = Bitcoin.req("https://coinbase.com/api/v1/account/balance")
        return Decimal(obj['amount'])

    @staticmethod
    # Returns the amount in USD that the bitcoins were exchanged for
    def convert_all():
        raise NotImplementedError()

