from common.pyreact import createElement as el, Modal
from common.pymui import Box, Paper, TextField, Button, Typography
from common.pymui import IconButton, CloseIcon
from main.appData import appname
from main.appTheme import Flexbox, FlexboxCenter, modalStyles


def Login(props):
    onClose = props['onClose']
    onLogin = props['onLogin']
    username = props['username']
    password = props['password']
    setUsername = props['setUsername']
    setPassword = props['setPassword']
    modalState = props['modalState']

    def login(event):
        event.preventDefault()
        onLogin()

    def handleUsernameChange(event):
        target = event['target']
        setUsername(target['value'])

    def handlePasswordChange(event):
        target = event['target']
        setPassword(target['value'])

    return el(Modal, {'isOpen': modalState,
                      'onRequestClose': onClose,
                      'style': modalStyles,
                      'ariaHideApp': False,
                     },
              el(FlexboxCenter, {'maxWidth': '300px'},
                 el(Box, None,
                    el(Flexbox, {'justifyContent': 'space-between',
                                 'alignItems': 'center'},
                       el(Typography, {'variant': 'h6',
                                       'width': '40%',
                                       'color': 'primary'}, appname),
                       el(IconButton, {'edge': 'end',
                                       'color': 'primary',
                                       'onClick': onClose}, el(CloseIcon, None))
                      ),
                    el(Paper, {'elevation': 2, 'style': {'padding': '1rem'}},
                       el('form', {'onSubmit': login},
                          el(TextField, {'label': 'Login Name',
                                         'variant': 'outlined',
                                         'fullWidth': True,
                                         'value': username,
                                         'onChange': handleUsernameChange,
                                         'autoFocus': True
                                        }
                            ),
                          el(TextField, {'label': 'Password',
                                         'variant': 'outlined',
                                         'fullWidth': True,
                                         'type': 'password',
                                         'value': password,
                                         'onChange': handlePasswordChange
                                        }
                            ),
                          el(Button, {'type': 'submit',
                                      'fullWidth': True,
                                      'style': {'minWidth': '10rem',
                                                'marginRight': '1rem',
                                                'marginTop': '1rem'},
                                     }, "Login"
                            ),
                         )
                      )
                   )
                )
             )

