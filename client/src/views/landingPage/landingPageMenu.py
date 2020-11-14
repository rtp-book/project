from common.pyreact import useState, createElement as el, Fragment
from common.pymui import Menu, MenuItem

lookup_tables = ['Categories', 'Publishers', 'Conditions', 'Formats']


def LandingPageMenu(props):
    mainMenu = props['mainMenu']
    mainMenuClose = props['mainMenuClose']
    aboutModalOpen = props['aboutModalOpen']
    logout = props['logout']
    isLoggedIn = props['isLoggedIn']

    lookupMenu, setLookupMenu = useState(None)

    def lookupMenuOpen(event):
        setLookupMenu(event['currentTarget'])

    def lookupMenuClose():
        setLookupMenu(None)
        mainMenuClose()

    def handleLookup(event):
        value = event['currentTarget']['textContent']
        lookupMenuClose()
        print("Lookup Table:", value)

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
                 el(MenuItem, {'onClick': lookupMenuOpen}, "Lookup  Tables"),
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
                 [el(MenuItem, {'key': table,
                                'onClick': handleLookup
                               }, table) for table in lookup_tables
                 ],
                )
             )

