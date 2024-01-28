from base64 import b64encode as __b64encode__
from base64 import b64decode as __b64decode__
from hashlib import md5 as __md5enc__

sb64dec = lambda x:__b64decode__(x.encode()).decode()
sb64enc = lambda x:__b64encode__(x.encode()).decode()
md5enc = lambda x:__md5enc__(x.encode()).hexdigest()