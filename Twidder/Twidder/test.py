import hashlib
import hmac
import base64

message = bytes('Message', 'utf-8')
secret = bytes('secret', 'utf-8')

signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
print(signature)
