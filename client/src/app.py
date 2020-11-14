from common.pyreact import render, useState, createElement as el, ReactGA
from common.pymui import ThemeProvider
from common.jsutils import setTitle
from main.appTheme import theme
from main.appData import gaid
from views.bookList.bookListView import BookList
from views.landingPage.landingPageView import LandingPage


ReactGA.initialize(gaid, {'titleCase': False, 'debug': False,
                         'gaOptions': {'siteSpeedSampleRate': 100}}
                  )


def App(props):
    setTitle(props['title'])

    booksShow, setBooksShow = useState(False)

    pathname = '/books' if booksShow else '/'

    router = {
        '/': LandingPage,
       '/books': BookList,
    }

    return el(ThemeProvider, {'theme': theme},
              el(router[pathname], {'setBooksShow': setBooksShow})
             )


render(App, {'title': "Books"}, 'root')

