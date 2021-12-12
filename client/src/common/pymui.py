from common.pyreact import react_component

# __pragma__ ('skip')
from common import require
# __pragma__ ('noskip')


# Icons
MenuIcon = react_component(require('@material-ui/icons/Menu')['default'])
CloseIcon = react_component(require('@material-ui/icons/Close')['default'])
AddIcon = react_component(require('@material-ui/icons/AddCircle')['default'])

# Basic components
Button = react_component(require('@material-ui/core/Button')['default'])
ButtonGroup = react_component(require('@material-ui/core/ButtonGroup')['default'])
IconButton = react_component(require('@material-ui/core/IconButton')['default'])
InputLabel = react_component(require('@material-ui/core/InputLabel')['default'])
OutlinedInput = react_component(require('@material-ui/core/OutlinedInput')['default'])
TextField = react_component(require('@material-ui/core/TextField')['default'])
Select = react_component(require('@material-ui/core/Select')['default'])
muiBox = require('@material-ui/core/Box')['default']
Box = react_component(muiBox)
Toolbar = react_component(require('@material-ui/core/Toolbar')['default'])
AppBar = react_component(require('@material-ui/core/AppBar')['default'])
Typography = react_component(require('@material-ui/core/Typography')['default'])
Divider = react_component(require('@material-ui/core/Divider')['default'])
Container = react_component(require('@material-ui/core/Container')['default'])
Input = react_component(require('@material-ui/core/Input')['default'])
Tooltip = react_component(require('@material-ui/core/Tooltip')['default'])
Menu = react_component(require('@material-ui/core/Menu')['default'])
MenuItem = react_component(require('@material-ui/core/MenuItem')['default'])
Paper = react_component(require('@material-ui/core/Paper')['default'])
CircularProgress = react_component(require('@material-ui/core/CircularProgress')['default'])
Link = react_component(require('@material-ui/core/Link')['default'])
Radio = react_component(require('@material-ui/core/Radio')['default'])
RadioGroup = react_component(require('@material-ui/core/RadioGroup')['default'])
FormControl = react_component(require('@material-ui/core/FormControl')['default'])
FormLabel = react_component(require('@material-ui/core/FormLabel')['default'])
FormControlLabel = react_component(require('@material-ui/core/FormControlLabel')['default'])

# Tables
TableContainer = react_component(require('@material-ui/core/TableContainer')['default'])
Table = react_component(require('@material-ui/core/Table')['default'])
TableHead = react_component(require('@material-ui/core/TableHead')['default'])
TableBody = react_component(require('@material-ui/core/TableBody')['default'])
TableFooter = react_component(require('@material-ui/core/TableFooter')['default'])
TableRow = react_component(require('@material-ui/core/TableRow')['default'])
TableCell = react_component(require('@material-ui/core/TableCell')['default'])

# Theming
ThemeProvider = react_component(require('@material-ui/styles/ThemeProvider')['default'])
createMuiTheme = require('@material-ui/core/styles/createMuiTheme')['default']
useTheme = require('@material-ui/styles/useTheme')['default']
styled = require('@material-ui/styles/styled')['default']
makeStyles = require('@material-ui/styles/makeStyles')['default']
colors = require('@material-ui/core/colors')


# notistack
notistack = require('notistack')

SnackbarProvider = react_component(notistack.SnackbarProvider)
useSnackbar = notistack.useSnackbar
