import uuid


def uuidgen(config):
    def thegenerator():
        while(True):
            yield str(uuid.uuid4())

    return thegenerator()


GENERATORS = {'uuidgen': uuidgen}
