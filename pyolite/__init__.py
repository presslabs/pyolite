try:
    from .pyolite import Pyolite
except ImportError as exp:
    # need this in order to make versioneer work
    pass
