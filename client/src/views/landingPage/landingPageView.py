from common.pyreact import useState, createElement as el
from common.pymui import Container, Paper, Typography
from common.pymui import IconButton, MenuIcon, Link
from main.appTheme import Flexbox, FlexboxCenter
from main.aboutModal import About
from main.appData import appname
from views.landingPage.landingPageMenu import LandingPageMenu


def LandingPage(props):
    setBooksShow = props['setBooksShow']

    mainMenu, setMainMenu = useState(None)
    aboutShow, setAboutShow = useState(False)

    def mainMenuOpen(event):
        setMainMenu(event['currentTarget'])

    def mainMenuClose():
        setMainMenu(None)

    def aboutModalOpen():
        setAboutShow(True)

    return el(Container, {'maxWidth': 'md'},
              el(Paper, {'style': {'padding': '1rem'}},
                 el(Flexbox, {'alignItems': 'center'},
                    el(IconButton, {'edge': 'start',
                                    'color': 'inherit',
                                    'onClick': mainMenuOpen
                                   }, el(MenuIcon, None)
                      ),
                    el(Typography, {'variant': 'h5'}, appname)
                   )
                ),
              el(LandingPageMenu, {'mainMenu': mainMenu,
                                   'mainMenuClose': mainMenuClose,
                                   'aboutModalOpen': aboutModalOpen}
                ),
              el(Paper, {'style': {'padding': '0.5rem',
                                   'marginTop': '1rem'}
                        },
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'},
                       el(Link, {'href': '#',
                                 'variant': 'h5',
                                 'onClick': lambda: setBooksShow(True)
                                }, "Books")
                      ),
                   ),
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'},
                       el(Link, {'href': '#'}, "Login")
                      )
                   ),
                ),
              el(About, {'onClose': lambda: setAboutShow(False),
                         'modalState': aboutShow}
                )
             )

