try:
    from .pyolite import Pyolite
except ImportError:
    # need this in order to make versioneer work
    pass

from .version import get_versions

__version__ = get_versions()['version']
del get_versions
