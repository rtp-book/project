from common.pyreact import Modal, useState, useEffect, createElement as el
from common.pymui import Typography, AppBar, Toolbar, Box, Paper
from common.pymui import IconButton, CloseIcon, useSnackbar
from common.urlutils import fetch
from main.appTheme import modalStyles
from views.lookupTable.lookupList import ItemsList

lookup_tables = [
    {'name': 'Categories', 'fields': ['Category'], 'sort': 'Category'},
    {'name': 'Publishers', 'fields': ['Publisher'], 'sort': 'Publisher'},
    {'name': 'Conditions', 'fields': ['Code', 'Condition'], 'sort': 'ID}'},
    {'name': 'Formats', 'fields': ['Format'], 'sort': 'Format'}
]


def LookupTable(props):
    onClose = props['onClose']
    table_name = props['table']

    table_info = next(
        (table for table in lookup_tables if table['name'] == table_name),
        {})
    table_fields = table_info['fields']
    table_sort = table_info['sort']
    modalState = bool(table_name)

    items, setItems = useState([])

    snack = useSnackbar()

    def on_update_error():
        snack.enqueueSnackbar("Error updating lookup table!", 
                              {'variant': 'error'})
        getItems()

    def on_update_success():
        snack.enqueueSnackbar("Lookup table updated!", {'variant': 'success'})
        getItems()

    def saveItem(item):
        # If all non-ID values are empty, then delete record
        if len(''.join([val for key, val in item.items() if key != 'ID'])) == 0:
            if not item.get('ID', None):
                getItems()  # Probably an unmodified record so just refresh list
            else:
                fetch(f"/api/lookup/{table_name}", on_update_success,
                      method='DELETE', data=item, onError=on_update_error)
        else:
            fetch(f"/api/lookup/{table_name}", on_update_success,
                  method='POST', data=item, onError=on_update_error)

    def getItems():
        def _getItems(data):
            item_list = data if data else []
            if len(item_list) > 0:
                item_list.sort(key=lambda item: item[table_sort])
                setItems(item_list)
            else:
                setItems([])

        if table_name:
            fetch(f"/api/lookup/{table_name}", _getItems)
        else:
            setItems([])

    useEffect(getItems, [table_name])

    return el(Modal, {'isOpen': modalState,
                      'style': modalStyles,
                      'ariaHideApp': False,
                     },
              el(AppBar, {'position': 'static',
                          'style': {'marginBottom': '0.5rem'}
                         },
                 el(Toolbar, {'variant': 'dense'},
                    el(Box, {'width': '100%'},
                       el(Typography, {'variant': 'h6'}, f"Table: {table_name}")
                      ),
                    el(IconButton, {'edge': 'end',
                                    'color': 'inherit',
                                    'onClick': onClose
                                   }, el(CloseIcon, None)
                      ),
                   ),
                ),
              el(Paper, {'style': {'padding': '0.5rem', 'marginTop': '0.8rem'}},
                 el(ItemsList, {'items': items,
                                'fields': table_fields,
                                'saveItem': saveItem,
                                'setItems': setItems})
                )
             )

