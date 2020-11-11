from common.pyreact import render, useState, createElement as el
from common.pymui import ThemeProvider, Paper, Typography, Container, Link
from common.jsutils import setTitle
from main.appTheme import theme, Flexbox, FlexboxCenter
from main.aboutModal import About
from main.appData import appname

def App(props):
    setTitle(props['title'])

    aboutShow, setAboutShow = useState(False)

    def handleClickAbout(event):
        event.preventDefault()
        setAboutShow(True)

    return el(ThemeProvider, {'theme': theme},
              el(Container, None,
                 el(Paper, {'style': {'padding': '1rem'}},
                    el(Flexbox, {'alignItems': 'center'},
                       el(Typography, {'variant': 'h5'}, appname)
                      )
                   ),
                 el(Paper, {'style': {'padding': '0.5rem',
                                      'marginTop': '1rem'}
                           },
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5'}, "Books")
                      ),
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5',
                                 'onClick': handleClickAbout
                                }, "About")
                      ),
                    el(FlexboxCenter, None,
                       el(Link, {'href': '#', 'variant': 'h5'}, "Login")
                      )
                   ),
                 el(About, {'onClose': lambda: setAboutShow(False),
                            'modalState': aboutShow}
                   ),
                )
             )

render(App, {'title': "Books"}, 'root')

