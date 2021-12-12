# __pragma__ ('skip')
from common import require, document, window, __new__
# __pragma__ ('noskip')


# Load React and ReactDOM JavaScript libraries into local namespace
React = require('react')
ReactDOM = require('react-dom')


# Map React javaScript objects to Python identifiers
# createElement = React.createElement
useState = React.useState
useEffect = React.useEffect
createContext = React.createContext
useContext = React.useContext


def react_component(component):
    def react_element(props, *children):
        return React.createElement(component, props, *children)

    return react_element


Fragment = react_component(React.Fragment)

Modal = react_component(require('react-modal'))
ReactGA = require('react-ga')

Form = react_component('form')
Label = react_component('label')
Input = react_component('input')
Ol = react_component('ol')
Li = react_component('li')
Option = react_component('option')
Button = react_component('button')
Div = react_component('div')
Span = react_component('span')
P = react_component('p')
A = react_component('a')
Img = react_component('img')
H1 = react_component('h1')
H2 = react_component('h2')


def render(root_component, props, container):
    def main():
        querystring = window.location.search
        params = __new__(window.URLSearchParams(querystring)).entries()
        new_props = {'pathname': window.location.pathname,
                     'params': {p[0]: p[1] for p in params if p}}
        new_props.update(props)
        ReactDOM.render(
            root_component(new_props),
            document.getElementById(container)
        )

    document.addEventListener('DOMContentLoaded', main)
    window.addEventListener('popstate', main)
