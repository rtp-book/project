from common.pyreact import useState, react_component, Fragment, useContext
from common.pymui import Menu, MenuItem
from main import UserCtx
from views.lookupTable.lookupView import lookup_tables


@react_component
def LandingPageMenu(props):
    mainMenu = props['mainMenu']
    mainMenuClose = props['mainMenuClose']
    setLookupModal = props['setLookupModal']
    aboutModalOpen = props['aboutModalOpen']

    ctx = useContext(UserCtx)
    logout = ctx['logout']
    isLoggedIn = ctx['isLoggedIn']

    lookupMenu, setLookupMenu = useState(None)

    def lookupMenuOpen(event):
        setLookupMenu(event['currentTarget'])

    def lookupMenuClose():
        setLookupMenu(None)
        mainMenuClose()

    def handleLookup(event):
        value = event['currentTarget']['textContent']
        lookupMenuClose()
        setLookupModal(value)

    def handleAbout():
        mainMenuClose()
        aboutModalOpen()

    def handleLogout():
        mainMenuClose()
        logout()

    return Fragment(None,
                    Menu({'id': 'main-menu',
                          'anchorEl': mainMenu,
                          'keepMounted': True,
                          'open': bool(mainMenu),
                          'onClose': mainMenuClose,
                          },
                         MenuItem({'onClick': lookupMenuOpen,
                                   'disabled': not isLoggedIn}, "Lookup  Tables"),
                         MenuItem({'onClick': handleAbout}, "About"),
                         MenuItem({'onClick': handleLogout,
                                   'disabled': not isLoggedIn}, "Logout"),
                         ),
                    Menu({'id': 'lookup-menu',
                          'anchorEl': lookupMenu,
                          'keepMounted': True,
                          'open': bool(lookupMenu),
                          'onClose': lookupMenuClose,
                          'transformOrigin': {'vertical': 'top',
                                              'horizontal': 'center'},
                          },
                         [MenuItem({'key': table['name'],
                                    'onClick': handleLookup
                                    }, table['name']) for table in lookup_tables
                          ],
                         )
                    )
