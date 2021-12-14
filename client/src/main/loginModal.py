from common.pyreact import react_component, Modal, Form
from common.pymui import Box, Paper, TextField, Button, Typography
from common.pymui import IconButton, CloseIcon
from main.appData import appname
from main.appTheme import Flexbox, FlexboxCenter, modalStyles


@react_component
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

    return Modal({'isOpen': modalState,
                  'onRequestClose': onClose,
                  'style': modalStyles,
                  'ariaHideApp': False,
                  },
                 FlexboxCenter({'maxWidth': '300px'},
                               Box(None,
                                   Flexbox({'justifyContent': 'space-between',
                                            'alignItems': 'center'},
                                           Typography({'variant': 'h6',
                                                       'width': '40%',
                                                       'color': 'primary'}, appname),
                                           IconButton({'edge': 'end',
                                                       'color': 'primary',
                                                       'onClick': onClose}, CloseIcon(None))
                                           ),
                                   Paper({'elevation': 2, 'style': {'padding': '1rem'}},
                                         Form({'onSubmit': login},
                                              TextField({'label': 'Login Name',
                                                         'variant': 'outlined',
                                                         'fullWidth': True,
                                                         'value': username,
                                                         'onChange': handleUsernameChange,
                                                         'autoFocus': True
                                                         }
                                                        ),
                                              TextField({'label': 'Password',
                                                         'variant': 'outlined',
                                                         'fullWidth': True,
                                                         'type': 'password',
                                                         'value': password,
                                                         'onChange': handlePasswordChange
                                                         }
                                                        ),
                                              Button({'type': 'submit',
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
