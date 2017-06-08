try:
    from .pyolite import Pyolite
except ImportError:
    # need this in order to make versioneer work
    pass
