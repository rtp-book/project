from common.pyreact import render, createElement as el, ReactGA
from common.pyreact import useState, useEffect
from common.pymui import ThemeProvider, SnackbarProvider
from common.jsutils import setTitle, console
from common.urlutils import fetch
from main import UserCtx
from main.appTheme import theme
from main.appData import gaid
from views.bookList.bookListView import BookList
from views.landingPage.landingPageView import LandingPage


ReactGA.initialize(gaid, {'titleCase': False, 'debug': False,
                         'gaOptions': {'siteSpeedSampleRate': 100}}
                  )


def App(props):
    user, setUser = useState("")

    setTitle(props['title'])

    booksShow, setBooksShow = useState(False)

    pathname = '/books' if booksShow else '/'

    router = {
        '/': LandingPage,
        '/books': BookList,
    }

    isLoggedIn = len(user) > 0

    def login(username):
        setUser(username)

    def logout():
        setUser("")
        fetch('/api/logout')

    def validateSession():
        def validated():
            def _setuser(data):
                login(data['user'])

            if not isLoggedIn:
                fetch('/api/whoami', _setuser,
                      onError=console.error,
                      redirect=False
                     )

        def notValidated(error):
            if len(user) > 0:
                setUser("")

        fetch('/api/ping', validated, onError=notValidated, redirect=False)


    useEffect(validateSession, [])

    user_ctx = {'user': user,
                'login': login,
                'logout': logout,
                'isLoggedIn': isLoggedIn
               }

    return el(ThemeProvider, {'theme': theme},
              el(SnackbarProvider, {'maxSnack': 3},
                 el(UserCtx.Provider, {'value': user_ctx},
                    el(router[pathname], {'setBooksShow': setBooksShow}
                      )
                   )
                )
             )


render(App, {'title': "Books"}, 'root')


