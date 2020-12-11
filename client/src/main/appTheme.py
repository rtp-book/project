from common.pyreact import createElement
from common.pymui import createMuiTheme, colors
from common.pymui import Box, styled, TextField

theme = createMuiTheme({
    'overrides': {
        'MuiDivider': {
            'root': {
                'margin': '0.8rem',
            }
        },
        'MuiTextField': {
            'root': {
                'marginRight': '0.5rem',
            }
        },
    },
    'palette': {
        'primary': colors['teal'],
        'secondary': colors['pink'],
        'altPrimary': {
            'main': colors['cyan'][700],
            'contrastText': colors['common']['white'],
        },
        'altSecondary': {
            'main': colors['cyan'][400],
            'contrastText': colors['common']['white'],
        },
        'warning': colors['yellow'],
        'error': colors['red'],
    },
    'props': {
        'MuiButton': {
            'variant': 'contained',
            'color': 'primary',
            'style': {'minWidth': '6rem', 'margin': '0.3rem'},
        },
        'MuiTextField': {
            'variant': 'outlined',
            'type': 'text',
            'fullWidth': True,
            'InputLabelProps': {'shrink': True},
            'InputProps': {'margin': 'dense'},
            'margin': 'dense',
        },
        'MuiPaper': {
            'elevation': 2
        },
        'MuiTable': {
            'stickyHeader': True,
            'size': 'small'
        },
        'MuiTableCell': {
            'size': 'small'
        },
    },
})


def ROTextField(props):
    new_props = {'type': 'text', 'fullWidth': True, 'disabled': True}
    new_props.update(props)
    return createElement(TextField, new_props)


Flexbox = styled(Box)({
    'display': 'flex',
})

FlexboxCenter = styled(Box)({
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center'
})

modalStyles = {
    'overlay': {'zIndex': 1000},
    'content': {
        'top': '35%',
        'left': '50%',
        'right': 'auto',
        'bottom': 'auto',
        'marginRight': '-50%',
        'transform': 'translate(-50%, -50%)'
    }
}


