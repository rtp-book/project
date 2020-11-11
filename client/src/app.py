from common.pyreact import render, createElement as el
from common.pymui import ThemeProvider, Paper, Typography, Container, Link
from common.jsutils import setTitle
from main.appTheme import theme, Flexbox, FlexboxCenter

APP_NAME = "Library Management System"

def App(props):
    setTitle(props['title'])

    return el(ThemeProvider, {'theme': theme},
              el(Container, {'maxWidth': 'md'},
                 el(Paper, {'style': {'padding': '1rem'}},
                    el(Flexbox, {'alignItems': 'center'},
                       el(Typography, {'variant': 'h5'}, APP_NAME)
                      )
                   ),
                 el(Paper, {'style': {'padding': '0.5rem',
                                      'marginTop': '1rem'}
                           },
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5'}, "Books")
                      ),
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5'}, "About")
                      ),
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5'}, "Login")
                      )
                   )
                )
             )

render(App, {'title': "Books"}, 'root')

