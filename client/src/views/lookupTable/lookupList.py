from common.pyreact import useState, createElement as el, Fragment
from common.pymui import Box, AddIcon, IconButton
from common.pymui import TableContainer, Table
from common.pymui import TableHead, TableBody, TableRow, TableCell


def ItemCell(props):
    value = props['value']

    return el(TableCell, None,
              el(Box, {'width': '10rem', 'whiteSpace': 'nowrap'}, value)
              )


def ItemRowVu(props):
    item = props['item']
    fields = props['fields']

    return el(TableRow, None,
              [el(ItemCell, {'key': field,
                             'value': item[field],
                             }) for field in fields]
             )


def ItemRows(props):
    items = props['items']
    fields = props['fields']

    def itemToRow(item):
        return el(ItemRowVu, {'key': item['ID'],
                              'item': item,
                              'fields': fields,
                             }
                 )

    if len(items) > 0:
        return el(Fragment, None,
                  [itemToRow(item) for item in items if item]
                 )
    else:
        return el(TableRow, {'key': '0'})


def ItemsList(props):
    items = props['items']
    fields = props['fields']

    def HeaderCols():
        return el(TableRow, None,
                  [el(TableCell, {'key': field, 'fields': fields}, field)
                   for field in fields]
                 )

    return el(TableContainer, {'style': {'maxHeight': '10.5rem'}},
              el(Table, {'size': 'small', 'stickyHeader': True},
                 el(TableHead, None,
                    el(HeaderCols, None),
                   ),
                 el(TableBody, None,
                    el(ItemRows, {'items': items,
                                  'fields': fields}
                      )
                   )
                )
             )

