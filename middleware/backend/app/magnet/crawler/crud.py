from libs import decorators

crawlers = decorators.Tag(tag="crawler", key_selector=lambda func: func.__name__)

