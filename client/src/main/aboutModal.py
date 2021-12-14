from common.pyreact import react_component, Modal, Img
from common.pymui import Paper, Typography, IconButton, CloseIcon, Divider
from main.appData import applogo, appname
from main.appTheme import Flexbox, FlexboxCenter, modalStyles
from version import version


@react_component
def About(props):
    modalState = props['modalState']
    onClose = props['onClose']

    return Modal({'isOpen': modalState,
                  'onRequestClose': onClose,
                  'style': modalStyles,
                  'ariaHideApp': False,
                  },
                 Flexbox({'justifyContent': 'space-between',
                          'alignItems': 'center'
                          },
                         Typography({'variant': 'h6', 'color': 'primary'}, "About"),
                         IconButton({'edge': 'end',
                                     'color': 'primary',
                                     'onClick': onClose
                                     }, CloseIcon(None)
                                    ),
                         ),
                 Paper({'style': {'padding': '1rem'}},
                       FlexboxCenter({'maxWidth': '400px'},
                                     Img({'src': applogo, 'width': '80%'})
                                     ),
                       ),
                 Paper({'style': {'padding': '0.5rem', 'marginTop': '1rem'}},
                       FlexboxCenter(None,
                                     Typography({'variant': 'h5'}, appname)
                                     ),
                       Divider({'style': {'marginTop': '0.5rem',
                                          'marginBottom': '0.5rem'}
                                }
                               ),
                       FlexboxCenter(None,
                                     Typography({'variant': 'h5'}, f"Version: {version}")
                                     ),
                       )
                 )
