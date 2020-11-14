from common.pyreact import useState, createElement as el, Fragment, useContext
from common.pymui import Menu, MenuItem
from main import UserCtx
from views.lookupTable.lookupView import lookup_tables


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

    return el(Fragment, None,
              el(Menu, {'id': 'main-menu',
                        'anchorEl': mainMenu,
                        'keepMounted': True,
                        'open': bool(mainMenu),
                        'onClose': mainMenuClose,
                       },
                 el(MenuItem, {'onClick': lookupMenuOpen,
                               'disabled': not isLoggedIn}, "Lookup  Tables"),
                 el(MenuItem, {'onClick': handleAbout}, "About"),
                 el(MenuItem, {'onClick': handleLogout,
                               'disabled': not isLoggedIn}, "Logout"),
                ),
              el(Menu, {'id': 'lookup-menu',
                        'anchorEl': lookupMenu,
                        'keepMounted': True,
                        'open': bool(lookupMenu),
                        'onClose': lookupMenuClose,
                        'transformOrigin': {'vertical': 'top',
                                            'horizontal': 'center'},
                       },
                 [el(MenuItem, {'key': table['name'],
                                'onClick': handleLookup
                               }, table['name']) for table in lookup_tables
                 ],
                )
             )


