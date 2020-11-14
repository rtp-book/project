from common.pyreact import useState, createElement as el, useEffect
from common.pymui import Container, Paper, Typography, useSnackbar
from common.pymui import IconButton, MenuIcon, Link
from common.urlutils import fetch
from main.appTheme import Flexbox, FlexboxCenter
from main.aboutModal import About
from main.appData import appname
from main.loginModal import Login
from views.landingPage.landingPageMenu import LandingPageMenu


def LandingPage(props):
    setBooksShow = props['setBooksShow']
    login = props['login']
    logout = props['logout']
    isLoggedIn = props['isLoggedIn']

    mainMenu, setMainMenu = useState(None)
    aboutShow, setAboutShow = useState(False)
    loginModal, setLoginModal = useState(False)
    username, setUsername = useState("")
    password, setPassword = useState("")

    snack = useSnackbar()

    def doLogin():
        def _login():
            login(username)
            snack.enqueueSnackbar("Login succeeded!", {'variant': 'success'})

        def _loginFailed():
            setLoginModal(True)
            snack.enqueueSnackbar("Login failed, please try again",
                                  {'variant': 'error'}
                                 )

        fetch("/api/login", _login,
              data={'username': username, 'password': password},
              method='POST',
              onError=_loginFailed
             )

        setLoginModal(False)

    def clearUser():
        if loginModal:
            setUsername("")
            setPassword("")

    def mainMenuOpen(event):
        setMainMenu(event['currentTarget'])

    def mainMenuClose():
        setMainMenu(None)

    def aboutModalOpen():
        setAboutShow(True)

    useEffect(clearUser, [loginModal])

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
                                   'aboutModalOpen': aboutModalOpen,
                                   'logout': logout,
                                   'isLoggedIn': isLoggedIn}
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
                       el(Link, {'href': '#',
                                 'onClick': lambda: setLoginModal(True)
                                }, "Login")
                      ) if not isLoggedIn else None
                   ),
                ),
              el(Login, {'onClose': lambda: setLoginModal(False),
                         'onLogin': doLogin,
                         'password': password,
                         'username': username,
                         'setUsername': lambda usr: setUsername(usr),
                         'setPassword': lambda pwd: setPassword(pwd),
                         'modalState': loginModal,
                        }
                ),
              el(About, {'onClose': lambda: setAboutShow(False),
                         'modalState': aboutShow}
                )
             )

