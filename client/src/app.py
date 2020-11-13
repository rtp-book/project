from common.pyreact import render, useState, createElement as el, ReactGA
from common.pymui import ThemeProvider, Paper, Typography, Container, Link
from common.jsutils import setTitle
from main.appTheme import theme, Flexbox, FlexboxCenter
from main.aboutModal import About
from main.appData import appname, gaid
from views.bookList.bookListView import BookList

ReactGA.initialize(gaid, {'titleCase': False, 'debug': False,
                         'gaOptions': {'siteSpeedSampleRate': 100}}
                  )


def App(props):
    setTitle(props['title'])

    aboutShow, setAboutShow = useState(False)
    booksShow, setBooksShow = useState(False)

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
                       el(Link, {'href': '#',
                                 'variant': 'h5',
                                 'onClick': lambda: setBooksShow(True)
                                }, "Books")
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
                ) if not booksShow else None,
              el(BookList, {'setBooksShow': setBooksShow}
                ) if booksShow else None,
             )


render(App, {'title': "Books"}, 'root')

