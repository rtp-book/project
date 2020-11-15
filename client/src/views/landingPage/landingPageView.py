from common.pyreact import useState, createElement as el, useEffect, useContext
from common.pymui import Container, Paper, Typography, useSnackbar
from common.pymui import IconButton, MenuIcon
from common.urlutils import fetch, Link, buildParams, spaRedirect
from main import UserCtx
from main.appTheme import Flexbox, FlexboxCenter
from main.aboutModal import About
from main.appData import appname
from main.loginModal import Login
from views.landingPage.landingPageMenu import LandingPageMenu
from views.lookupTable.lookupView import LookupTable


def LandingPage(props):
    params = dict(props['params'])
    pathname = props['pathname']

    show_login = params.get('login', 'hide') == 'show'

    uCtx = useContext(UserCtx)
    isLoggedIn = uCtx['isLoggedIn']
    login = uCtx['login']

    mainMenu, setMainMenu = useState(None)
    aboutShow, setAboutShow = useState(False)
    lookupModal, setLookupModal = useState(None)
    loginModal, setLoginModal = useState(False)
    username, setUsername = useState("")
    password, setPassword = useState("")

    snack = useSnackbar()

    def doLogin():
        def _login():
            login(username)
            snack.enqueueSnackbar("Login succeeded!", {'variant': 'success'})
            spaRedirect(redir)

        def _loginFailed():
            setLoginModal(True)
            snack.enqueueSnackbar("Login failed, please try again",
                                  {'variant': 'error'}
                                  )

        redir = params.get('redir', f"{pathname}{buildParams(params)}")
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

    useEffect(lambda: setLoginModal(show_login), [show_login])
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
                                   'setLookupModal':
                                       lambda tbl: setLookupModal(tbl),
                                   'aboutModalOpen': aboutModalOpen}
                ),
              el(Paper, {'style': {'padding': '0.5rem',
                                   'marginTop': '1rem'}
                        },
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'},
                       el(Link, {'to': '/books'}, "Books")
                      ),
                   ),
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'},
                       el(Link, {'to': '#',
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
                ),
              el(LookupTable, {'table': lookupModal,
                               'onClose': lambda: setLookupModal(None)}
                ) if lookupModal else None
             )

