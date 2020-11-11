from common.pyreact import createElement as el, Modal
from common.pymui import Paper, Typography, IconButton, CloseIcon, Divider
from main.appData import applogo, appname
from main.appTheme import Flexbox, FlexboxCenter, modalStyles
from version import version


def About(props):
    modalState = props['modalState']
    onClose = props['onClose']

    return el(Modal, {'isOpen': modalState,
                      'onRequestClose': onClose,
                      'style': modalStyles,
                      'ariaHideApp': False,
                     },
              el(Flexbox, {'justifyContent': 'space-between',
                           'alignItems': 'center'
                          },
                 el(Typography, {'variant': 'h6', 'color': 'primary'}, "About"),
                 el(IconButton, {'edge': 'end',
                                 'color': 'primary',
                                 'onClick': onClose
                                }, el(CloseIcon, None)
                   ),
                ),
              el(Paper, {'style': {'padding': '1rem'}},
                 el(FlexboxCenter, {'maxWidth': '400px'},
                    el('img', {'src': applogo, 'width': '80%'})
                   ),
                ),
              el(Paper, {'style': {'padding': '0.5rem', 'marginTop': '1rem'}},
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'}, appname)
                   ),
                 el(Divider, {'style': {'marginTop': '0.5rem',
                                        'marginBottom': '0.5rem'}
                             }
                   ),
                 el(FlexboxCenter, None,
                    el(Typography, {'variant': 'h5'}, f"Version: {version}")
                   ),
                )
             )

