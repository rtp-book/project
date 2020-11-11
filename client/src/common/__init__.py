# __pragma__ ('skip')

"""
These JavaScript builtin function and object stubs are just to
quiet the Python linter and are ignored by transcrypt as long
as they are imported inside of pragma skip/noskip lines.
"""

def require(lib):
    return lib

def __new__(obj):
    return obj

class JSON:
    stringify = None

class document:
    title = None
    getElementById = None
    addEventListener = None

class window:
    class console:
        log = None
        error = None
        warn = None

    alert = None
    confirm = None
    fetch = None
    history = None
    location = None
    addEventListener = None
    dispatchEvent = None
    PopStateEvent = None
    URLSearchParams = None
    encodeURIComponent = None

# __pragma__ ('noskip')

