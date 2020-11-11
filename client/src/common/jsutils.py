# __pragma__ ('skip')
from common import require, document, window
# __pragma__ ('noskip')


console = window.console
alert = window.alert
confirm = window.confirm

deepcopy = require('deepcopy')


def setTitle(title):
    document.title = title

