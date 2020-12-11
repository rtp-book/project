# __pragma__ ('skip')
from common import require, document, window, __new__
# __pragma__ ('noskip')


# Load React and ReactDOM JavaScript libraries into local namespace
React = require('react')
ReactDOM = require('react-dom')
ReactGA = require('react-ga')

Modal = require('react-modal')

# Map React javaScript objects to Python identifiers
createElement = React.createElement
useState = React.useState
useEffect = React.useEffect
createContext = React.createContext
useContext = React.useContext

Fragment = React.Fragment


def render(root_component, props, container):
    def main():
        querystring = window.location.search
        params = __new__(window.URLSearchParams(querystring)).entries()
        new_props = {'pathname': window.location.pathname,
                     'params': {p[0]: p[1] for p in params if p}}
        new_props.update(props)
        ReactDOM.render(
            React.createElement(root_component, new_props),
            document.getElementById(container)
        )

    document.addEventListener('DOMContentLoaded', main)
    window.addEventListener('popstate', main)

