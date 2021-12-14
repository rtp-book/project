from common.pyreact import render, ReactGA, useState, useEffect
from common.pyreact import react_component, HTML
from common.pymui import ThemeProvider, SnackbarProvider
from common.jsutils import setTitle, console
from common.urlutils import fetch, spaRedirect
from main import UserCtxProvider
from main.appTheme import theme
from main.appData import gaid
from views.bookList.bookListView import BookList
from views.landingPage.landingPageView import LandingPage

ReactGA.initialize(gaid, {'titleCase': False, 'debug': False,
                          'gaOptions': {'siteSpeedSampleRate': 100}}
                   )


@react_component
def App(props):
    title = props['title']
    pathname = props['pathname']

    user, setUser = useState("")

    setTitle(title)

    router = {
        '/': LandingPage,
        '/books': BookList,
    }

    route_is_valid = pathname in router
    isLoggedIn = len(user) > 0

    def login(username):
        setUser(username)

    def logout():
        setUser("")
        fetch('/api/logout', lambda: spaRedirect('/'))

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

        if route_is_valid:
            fetch('/api/ping', validated, onError=notValidated, redirect=False)

    user_ctx = {'user': user,
                'login': login,
                'logout': logout,
                'isLoggedIn': isLoggedIn
                }

    useEffect(validateSession, [])
    useEffect(lambda: ReactGA.pageview(pathname), [pathname])

    if route_is_valid:
        return ThemeProvider({'theme': theme},
                             SnackbarProvider({'maxSnack': 3},
                                              UserCtxProvider({'value': user_ctx},
                                                              router[pathname](props)
                                                              )
                                              )
                             )
    else:
        console.error(f"ERROR - Bad pathname for route: {props['pathname']}")
        return HTML.Div(None,
                        HTML.H1(None, "Page Not Found"),
                        HTML.P(None, f"Bad pathname: {props['pathname']}"),
                        HTML.Div(None, HTML.A({'href': "/"}, "Back to Home"))
                        )


render(App, {'title': "Books"}, 'root')
