from magnet.vendors import Linq, MiniDB
from libs import decorators

from .zaif import Zaif
from .bitflyer import Bitflyer
from .cryptowat import CryptowatchAPI


# exchanges: MiniDB = MiniDB()
exchanges = decorators.Tag(tag="exchange", key_selector=lambda obj: obj.name)

# register
exchanges(Bitflyer)
exchanges(Zaif)
# exchanges(CryptowatchAPI)
