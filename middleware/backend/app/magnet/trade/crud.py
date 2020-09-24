from libs import decorators

exchanges = decorators.Tag(tag="exchange", key_selector=lambda obj: obj.name)


